from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CartItem, Order
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer
from .services import get_or_create_cart, checkout
from .tasks import send_order_confirmation_email
import io
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from rest_framework.decorators import api_view, permission_classes

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return get_or_create_cart(self.request.user)

class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        cart = get_or_create_cart(self.request.user)
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data.get("quantity", 1)
        item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id, defaults={"quantity": quantity})
        if not created:
            item.quantity += quantity
            item.save()
        self.instance = item

class CartItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "item_id"
    def get_queryset(self):
        cart = get_or_create_cart(self.request.user)
        return cart.items.all()

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().order_by("-id")
        return Order.objects.filter(user=self.request.user).order_by("-id")

class CheckoutView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        try:
            order = checkout(request.user)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        send_order_confirmation_email.delay(order.id)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def order_receipt_pdf(request, pk):
    """
    GET /api/orders/<pk>/receipt.pdf
    Only owner of order or staff can access.
    """
    order = get_object_or_404(Order, pk=pk)
    print(f"Generating receipt for order {order.id} by user {request.user}")
    if request.user != order.user and not request.user.is_staff:
        raise Http404("Order not found")

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("YourStore Name", styles['Title']))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(f"Receipt for Order #{order.id}", styles['Heading2']))
    story.append(Spacer(1, 3*mm))

    meta_table_data = [
        ["Order ID:", str(order.id)],
        ["Status:", str(order.status)],
        ["Date:", order.created_at.strftime("%Y-%m-%d %H:%M:%S")],
        ["Customer:", f"{order.user.get_full_name() or order.user.email}"],
    ]
    meta_table = Table(meta_table_data, colWidths=[60*mm, 100*mm])
    meta_table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4*mm))

    items_data = [["#", "Product", "Qty", "Unit Price", "Line Total"]]
    for i, item in enumerate(order.items.all(), start=1):
        product_name = getattr(item, "product_name", getattr(item, "product", None) and getattr(item.product, "name", ""))
        qty = getattr(item, "quantity", 1)
        price = getattr(item, "price", 0)
        line_total = qty * float(price)
        items_data.append([str(i), product_name, str(qty), f"{float(price):.2f}", f"{line_total:.2f}"])

    items_data.append(["", "", "", "Total:", f"{float(order.total):.2f}"])

    colWidths = [10*mm, 80*mm, 20*mm, 30*mm, 30*mm]
    table = Table(items_data, colWidths=colWidths, hAlign='LEFT')
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-2), 0.25, colors.grey),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (2,1), (2,-1), "CENTER"),
        ("ALIGN", (3,1), (4,-1), "RIGHT"),
        ("SPAN", (0,-1), (2,-1)),
        ("ALIGN", (3,-1), (4,-1), "RIGHT"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph("Thank you for shopping with us!", styles['Normal']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("If you have any questions about this order, contact support@yourstore.example", styles['Normal']))

    # Build PDF
    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f"order_{order.id}_receipt.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"' 
    return response
