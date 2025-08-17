from decimal import Decimal
from .models import Cart, CartItem, Order, OrderItem, Payment
from django.db import transaction

def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

def mock_charge(amount: Decimal, user) -> dict:
    # Replace with Stripe integration as needed
    return {"status": "succeeded", "id": "txn_mock_12345"}

@transaction.atomic
def checkout(user):
    cart = get_or_create_cart(user)
    items = list(cart.items.select_related("product"))
    if not items:
        raise ValueError("Cart is empty")

    total = sum((i.product.price * i.quantity for i in items), start=Decimal("0.00"))
    charge = mock_charge(total, user)
    status = "paid" if charge["status"] == "succeeded" else "failed"

    order = Order.objects.create(user=user, total=total, status=status)
    for i in items:
        OrderItem.objects.create(order=order, product=i.product, quantity=i.quantity, price=i.product.price)
    Payment.objects.create(order=order, provider="mock", status=charge["status"], transaction_id=charge["id"])
    cart.items.all().delete()
    return order
