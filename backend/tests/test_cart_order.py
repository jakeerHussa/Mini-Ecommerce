import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from products.models import Category, Product

@pytest.mark.django_db
def test_cart_checkout_flow():
    user = User.objects.create_user("buyer", password="secret123")
    client = APIClient()
    # login
    r = client.post("/api/auth/token/", {"username":"buyer","password":"secret123"}, format="json")
    token = r.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    cat = Category.objects.create(name="Cat")
    owner = User.objects.create_user("owner", password="secret123")
    prod = Product.objects.create(name="Thing", price="5.00", category=cat, owner=owner)
    # add to cart
    r = client.post("/api/cart/items/", {"product_id": prod.id, "quantity":2}, format="json")
    assert r.status_code == 201
    # checkout
    r = client.post("/api/orders/checkout/")
    assert r.status_code == 201
    assert r.data["total"] == "10.00"
