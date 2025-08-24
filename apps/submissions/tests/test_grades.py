from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from apps.courses.models import Course, Lecture, Homework
from apps.submissions.models import Submission, Grade
from apps.users.models import User


class GradeTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="123", role="teacher")
        self.student = User.objects.create_user(username="student", password="123", role="student")

        self.teacher_token = str(AccessToken.for_user(self.teacher))
        self.student_token = str(AccessToken.for_user(self.student))

        self.course = Course.objects.create(title="Python", description="Learn Python")
        self.course.teachers.add(self.teacher)

        lecture = Lecture.objects.create(course=self.course, topic="Lesson 1")
        hw = Homework.objects.create(lecture=lecture, text="Task 1")

        self.submission = Submission.objects.create(
            homework=hw,
            student=self.student,
            answer_text="My solution"
        )

    def get_auth_headers(self, token):
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    def test_teacher_add_grade(self):
        url = reverse('grades-list')
        data = {"submission": self.submission.id, "grade": 5, "comment": "Well done"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Grade.objects.count(), 1)
        self.assertEqual(Grade.objects.first().grade, 5)
        self.assertEqual(Grade.objects.first().teacher, self.teacher)

    def test_student_cannot_add_grade(self):
        url = reverse('grades-list')
        data = {"submission": self.submission.id, "grade": 5, "comment": "I'll give myself 5"}
        response = self.client.post(url, data, **self.get_auth_headers(self.student_token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Grade.objects.count(), 0)

    def test_unauthenticated_user_cannot_add_grade(self):
        url = reverse('grades-list')
        data = {"submission": self.submission.id, "grade": 5, "comment": "Anonymous grade"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Grade.objects.count(), 0)

    def test_add_grade_with_invalid_submission(self):
        url = reverse('grades-list')
        data = {"submission": 999, "grade": 5, "comment": "Non-existent submission"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Grade.objects.count(), 0)

    def test_add_grade_with_invalid_grade_value(self):
        url = reverse('grades-list')
        data = {"submission": self.submission.id, "grade": 15, "comment": "Invalid grade"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Grade.objects.count(), 0)

    def test_teacher_can_update_grade(self):
        grade = Grade.objects.create(
            submission=self.submission,
            teacher=self.teacher,
            grade=4,
            comment="Initial comment"
        )

        url = reverse('grades-detail', kwargs={'pk': grade.id})
        data = {"grade": 5, "comment": "Updated comment"}
        response = self.client.patch(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        grade.refresh_from_db()
        self.assertEqual(grade.grade, 5)
        self.assertEqual(grade.comment, "Updated comment")
