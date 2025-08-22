from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from course.models import User, Course

class CourseTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="123", role="teacher")
        self.client.login(username="teacher", password="123")

    def test_create_course(self):
        url = reverse('course-list')
        data = {"title": "Python Basics", "description": "Intro to Python"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().title, "Python Basics")

    def test_get_courses(self):
        Course.objects.create(title="Django", description="Web framework")
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
