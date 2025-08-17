from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@shared_task
def send_order_confirmation_email(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return
    subject = f"Order #{order.id} Confirmation"
    body = f"Thanks for your purchase! Total: {order.total}. Status: {order.status}."
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [order.user.email or "test@example.com"])
