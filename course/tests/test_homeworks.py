from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from course.models import User, Course, Lecture

class LectureTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="123", role="teacher")
        self.client.login(username="teacher", password="123")
        self.course = Course.objects.create(title="Python", description="Learn Python")
        self.course.teachers.add(self.teacher)

    def test_add_lecture(self):
        url = reverse('lectures-list')
        data = {"course": self.course.id, "topic": "Intro"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lecture.objects.count(), 1)
