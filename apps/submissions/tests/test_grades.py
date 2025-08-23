from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from apps.courses.models import Course, Lecture, Homework
from apps.submissions.models import Submission, Grade
from apps.users.models import User

class GradeTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="123", role="teacher")
        self.student = User.objects.create_user(username="student", password="123", role="student")
        self.client.login(username="teacher", password="123")
        self.course = Course.objects.create(title="Python", description="Learn Python")
        self.course.teachers.add(self.teacher)
        lecture = Lecture.objects.create(course=self.course, topic="Lesson 1")
        hw = Homework.objects.create(lecture=lecture, text="Task 1")
        self.submission = Submission.objects.create(homework=hw, student=self.student, answer_text="My solution")

    def test_add_grade(self):
        url = reverse('grades-list')
        data = {"submission": self.submission.id, "grade": 5, "comment": "Well done"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Grade.objects.count(), 1)
