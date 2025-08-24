from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User


from rest_framework.test import APITestCase
from django.urls import reverse
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

    def test_login_jwt(self):
        user = User.objects.create_user(
            username="test",
            password="pass123",
            role="student"
        )
        url = reverse('token_obtain_pair')
        data = {"username": "test", "password": "pass123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_authenticated_request_with_jwt(self):
        user = User.objects.create_user(
            username="student",
            password="pass123",
            role="student"
        )
        login_url = reverse('token_obtain_pair')
        data = {"username": "student", "password": "pass123"}
        response = self.client.post(login_url, data, format="json")

        access_token = response.data["access"]

        # теперь делаем запрос с токеном
        courses_url = reverse("courses-list")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(courses_url)

        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])

