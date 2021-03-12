import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from CoffeeShopTask import models
from CoffeeShopTask import serializers


class LoginTestCase(APITestCase):
    def test_login(self):
        data = {"username": "Sajjad", "password": "s.vahedi"}
        response = self.client.post("/api-auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="", password="12345678",
                                             email='localhost@django-rest.com')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_product(self):
        data = {"name": "Espresso", "price": "18000"}
        response = self.client.post("/products/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_product(self):
        data = {"name": "Espresso", "price": "18000"}
        response = self.client.get("/products/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
