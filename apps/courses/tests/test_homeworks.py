from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from apps.courses.models import Course, Lecture, Homework
from apps.users.models import User


class HomeworkTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="123", role="teacher")
        self.student = User.objects.create_user(username="student", password="123", role="student")
        self.other_teacher = User.objects.create_user(username="other_teacher", password="123", role="teacher")

        self.teacher_token = str(AccessToken.for_user(self.teacher))
        self.student_token = str(AccessToken.for_user(self.student))
        self.other_teacher_token = str(AccessToken.for_user(self.other_teacher))

        self.course = Course.objects.create(title="Python", description="Learn Python")
        self.course.teachers.add(self.teacher)

        self.lecture = Lecture.objects.create(course=self.course, topic="Lesson 1")

    def get_auth_headers(self, token):
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    def test_teacher_can_add_homework(self):
        url = reverse('homeworks-list')
        data = {"lecture": self.lecture.id, "text": "Do exercises"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Homework.objects.count(), 1)
        self.assertEqual(Homework.objects.first().text, "Do exercises")
        self.assertEqual(Homework.objects.first().lecture, self.lecture)

    def test_student_cannot_add_homework(self):
        url = reverse('homeworks-list')
        data = {"lecture": self.lecture.id, "text": "Student homework"}
        response = self.client.post(url, data, **self.get_auth_headers(self.student_token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Homework.objects.count(), 0)

    def test_teacher_cannot_add_homework_to_other_teacher_lecture(self):
        other_course = Course.objects.create(title="Other Course", description="Other teacher's course")
        other_course.teachers.add(self.other_teacher)
        other_lecture = Lecture.objects.create(course=other_course, topic="Other Lecture")

        url = reverse('homeworks-list')
        data = {"lecture": other_lecture.id, "text": "Unauthorized homework"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))

        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])
        self.assertEqual(Homework.objects.count(), 0)

    def test_unauthenticated_user_cannot_add_homework(self):
        url = reverse('homeworks-list')
        data = {"lecture": self.lecture.id, "text": "Anonymous homework"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Homework.objects.count(), 0)

    def test_add_homework_with_missing_text(self):
        url = reverse('homeworks-list')
        data = {"lecture": self.lecture.id}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Homework.objects.count(), 0)

    def test_add_homework_with_missing_lecture(self):
        url = reverse('homeworks-list')
        data = {"text": "Homework without lecture"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Homework.objects.count(), 0)

    def test_add_homework_with_nonexistent_lecture(self):
        url = reverse('homeworks-list')
        data = {"lecture": 999, "text": "Homework for non-existent lecture"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Homework.objects.count(), 0)

    def test_get_homeworks_list(self):
        Homework.objects.create(lecture=self.lecture, text="Homework 1")
        Homework.objects.create(lecture=self.lecture, text="Homework 2")

        url = reverse('homeworks-list')
        response = self.client.get(url, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_homework_detail(self):
        homework = Homework.objects.create(lecture=self.lecture, text="Detailed homework")

        url = reverse('homeworks-detail', args=[homework.id])
        response = self.client.get(url, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], "Detailed homework")
        self.assertEqual(response.data['lecture'], self.lecture.id)

    def test_update_homework(self):
        homework = Homework.objects.create(lecture=self.lecture, text="Old text")

        url = reverse('homeworks-detail', args=[homework.id])
        data = {"text": "Updated text"}
        response = self.client.patch(url, data, **self.get_auth_headers(self.teacher_token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        homework.refresh_from_db()
        self.assertEqual(homework.text, "Updated text")

    def test_delete_homework(self):
        homework = Homework.objects.create(lecture=self.lecture, text="To delete")

        url = reverse('homeworks-detail', args=[homework.id])
        response = self.client.delete(url, **self.get_auth_headers(self.teacher_token))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Homework.objects.count(), 0)
