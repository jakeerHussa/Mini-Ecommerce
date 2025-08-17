import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from products.models import Category

@pytest.mark.django_db
def test_register_and_create_product():
    client = APIClient()
    # register
    r = client.post("/api/auth/register/", {"username":"u1","email":"u1@x.com","password":"secret123"}, format="json")
    assert r.status_code == 201
    # login
    r = client.post("/api/auth/token/", {"username":"u1","password":"secret123"}, format="json")
    assert r.status_code == 200
    token = r.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    cat = Category.objects.create(name="Cat1")
    # create product
    r = client.post("/api/products/", {"name":"P1","price":"9.99","category_id":cat.id}, format="json")
    assert r.status_code == 201
    pid = r.data["id"]
    # edit product
    r = client.patch(f"/api/products/{pid}/", {"price":"12.00"}, format="json")
    assert r.status_code == 200
