from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from apps.courses.models import Course, Lecture, Homework
from apps.submissions.models import Submission, Grade
from apps.users.models import User


class PermissionTests(APITestCase):
    def setUp(self):
        self.teacher1 = User.objects.create_user(username="teacher1", password="123", role="teacher")
        self.teacher2 = User.objects.create_user(username="teacher2", password="123", role="teacher")
        self.student = User.objects.create_user(username="student", password="123", role="student")

        self.teacher1_token = str(AccessToken.for_user(self.teacher1))
        self.teacher2_token = str(AccessToken.for_user(self.teacher2))
        self.student_token = str(AccessToken.for_user(self.student))

        self.course = Course.objects.create(title="Python", description="Learn Python")
        self.course.teachers.add(self.teacher1)

    def get_auth_headers(self, token):
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    def test_student_cannot_create_course(self):
        url = reverse("courses-list")
        data = {"title": "HackCourse", "description": "Should not work"}
        response = self.client.post(url, data, **self.get_auth_headers(self.student_token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_create_course(self):
        url = reverse("courses-list")
        data = {"title": "Django", "description": "Web framework"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher1_token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)  # Один из setUp + новый

    def test_teacher_cannot_edit_other_teacher_course(self):
        url = reverse("courses-detail", args=[self.course.id])
        data = {"title": "Hacked course"}
        response = self.client.patch(url, data, **self.get_auth_headers(self.teacher2_token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_edit_own_course(self):
        url = reverse("courses-detail", args=[self.course.id])
        data = {"title": "Updated Python Course"}
        response = self.client.patch(url, data, **self.get_auth_headers(self.teacher1_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Updated Python Course")

    def test_student_cannot_create_lecture(self):
        url = reverse("lectures-list")
        data = {"course": self.course.id, "topic": "Hack lecture"}
        response = self.client.post(url, data, **self.get_auth_headers(self.student_token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_create_lecture(self):
        url = reverse("lectures-list")
        data = {"course": self.course.id, "topic": "Valid lecture"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher1_token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lecture.objects.count(), 1)

    def test_student_cannot_grade_submission(self):
        lecture = Lecture.objects.create(course=self.course, topic="Lesson 1")
        hw = Homework.objects.create(lecture=lecture, text="Task 1")
        sub = Submission.objects.create(homework=hw, student=self.student, answer_text="My answer")

        url = reverse("grades-list")
        data = {"submission": sub.id, "grade": 5, "comment": "Self grade"}
        response = self.client.post(url, data, **self.get_auth_headers(self.student_token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Grade.objects.count(), 0)

    def test_teacher_can_grade_submission(self):
        lecture = Lecture.objects.create(course=self.course, topic="Lesson 1")
        hw = Homework.objects.create(lecture=lecture, text="Task 1")
        sub = Submission.objects.create(homework=hw, student=self.student, answer_text="My answer")

        url = reverse("grades-list")
        data = {"submission": sub.id, "grade": 4, "comment": "Ok"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher1_token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Grade.objects.count(), 1)
        self.assertEqual(Grade.objects.first().grade, 4)

    def test_teacher_cannot_grade_own_submission(self):
        lecture = Lecture.objects.create(course=self.course, topic="Lesson 1")
        hw = Homework.objects.create(lecture=lecture, text="Task 1")
        sub = Submission.objects.create(homework=hw, student=self.teacher2, answer_text="Teacher's answer")

        url = reverse("grades-list")
        data = {"submission": sub.id, "grade": 5, "comment": "Grade myself"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher2_token))

        self.assertEqual(Grade.objects.count(), 0)

        self.assertFalse(response.status_code // 100 == 2)

        self.assertTrue(response.status_code // 100 == 4)

    def test_unauthenticated_user_cannot_access_protected_endpoints(self):
        endpoints = [
            reverse("courses-list"),
            reverse("lectures-list"),
            reverse("grades-list"),
        ]

        for url in endpoints:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
