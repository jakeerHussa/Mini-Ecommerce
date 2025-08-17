from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartView, CartItemCreateView, CartItemUpdateDeleteView, CheckoutView, OrderViewSet, order_receipt_pdf

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/', CartItemCreateView.as_view(), name='cart_item_add'),
    path('cart/items/<int:item_id>/', CartItemUpdateDeleteView.as_view(), name='cart_item_update_delete'),
    path('orders/checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/<int:pk>/receipt.pdf', order_receipt_pdf, name='order-receipt-pdf'),

]
urlpatterns += router.urls
