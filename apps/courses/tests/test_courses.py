from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User


class AuthTests(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            "username": "ivan",
            "email": "ivan@example.com",
            "password": "qwerty123",
            "role": "student"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["role"], "student")

    def test_login(self):
        user = User.objects.create_user(username="test", password="pass123", role="student")
        url = reverse('login')
        data = {"username": "test", "password": "pass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
