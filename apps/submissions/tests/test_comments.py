from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from apps.courses.models import Course, Lecture, Homework
from apps.submissions.models import Submission, Grade, GradeComment
from apps.users.models import User

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from apps.users.models import User
from apps.courses.models import Course, Lecture, Homework
from apps.submissions.models import Submission, Grade, GradeComment


class GradeCommentTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="123", role="teacher")
        self.student = User.objects.create_user(username="student", password="123", role="student")

        self.teacher_token = str(AccessToken.for_user(self.teacher))
        self.student_token = str(AccessToken.for_user(self.student))

        self.course = Course.objects.create(title="Python", description="Learn Python")
        self.course.teachers.add(self.teacher)

        self.lecture = Lecture.objects.create(course=self.course, topic="Lesson 1")
        self.homework = Homework.objects.create(lecture=self.lecture, text="Task 1")

        self.submission = Submission.objects.create(
            homework=self.homework,
            student=self.student,
            answer_text="My solution"
        )

        self.grade = Grade.objects.create(
            submission=self.submission,
            teacher=self.teacher,
            grade=5,
            comment="Nice work"
        )

    def get_auth_headers(self, token):
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    def test_student_add_comment(self):
        url = reverse("comments-list")
        data = {"grade": self.grade.id, "text": "Thx for chk!"}
        response = self.client.post(url, data, **self.get_auth_headers(self.student_token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GradeComment.objects.count(), 1)
        self.assertEqual(GradeComment.objects.first().text, "Thx for chk!")
        self.assertEqual(GradeComment.objects.first().author, self.student)

    def test_teacher_add_comment(self):
        url = reverse("comments-list")
        data = {"grade": self.grade.id, "text": "Next time try to optimize the code"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GradeComment.objects.count(), 1)
        self.assertEqual(GradeComment.objects.first().author, self.teacher)

    def test_student_cannot_comment_other_students_grade(self):
        other_student = User.objects.create_user(username="kate", password="123", role="student")
        other_student_token = str(AccessToken.for_user(other_student))

        other_submission = Submission.objects.create(
            homework=self.homework,
            student=other_student,
            answer_text="Other"
        )
        other_grade = Grade.objects.create(
            submission=other_submission,
            teacher=self.teacher,
            grade=4
        )

        url = reverse("comments-list")
        data = {"grade": other_grade.id, "text": "ooooopsss"}
        response = self.client.post(url, data, **self.get_auth_headers(self.student_token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(GradeComment.objects.count(), 0)

    def test_unauthenticated_user_cannot_comment(self):
        url = reverse("comments-list")
        data = {"grade": self.grade.id, "text": "Anon comment"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(GradeComment.objects.count(), 0)

    def test_comment_creation_with_invalid_token(self):
        url = reverse("comments-list")
        data = {"grade": self.grade.id, "text": "Comment with invalid token"}
        response = self.client.post(url, data, **{'HTTP_AUTHORIZATION': 'Bearer invalid_token'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(GradeComment.objects.count(), 0)
