from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from apps.courses.models import Course
from apps.users.models import User


class CourseTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="123", role="teacher")
        self.student = User.objects.create_user(username="student", password="123", role="student")

        self.teacher_token = str(AccessToken.for_user(self.teacher))
        self.student_token = str(AccessToken.for_user(self.student))

    def get_auth_headers(self, token):
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    def test_teacher_can_create_course(self):
        url = reverse('courses-list')
        data = {"title": "Python Basics", "description": "Intro to Python"}
        response = self.client.post(url, data, format='json', **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().title, "Python Basics")

        course = Course.objects.get()
        self.assertTrue(course.teachers.filter(id=self.teacher.id).exists())

    def test_student_cannot_create_course(self):
        url = reverse('courses-list')
        data = {"title": "Student Course", "description": "Should not work"}
        response = self.client.post(url, data, format='json', **self.get_auth_headers(self.student_token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.count(), 0)

    def test_unauthenticated_user_cannot_create_course(self):
        url = reverse('courses-list')
        data = {"title": "Anonymous Course", "description": "Should not work"}
        response = self.client.post(url, data, format='json')  # Без токена
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Course.objects.count(), 0)

    def test_get_courses(self):
        course = Course.objects.create(title="Django", description="Web framework")
        course.teachers.add(self.teacher)

        url = reverse('courses-list')
        response = self.client.get(url, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Django")

    def test_get_courses_unauthenticated(self):
        course = Course.objects.create(title="Django", description="Web framework")
        course.teachers.add(self.teacher)

        url = reverse('courses-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_course_detail(self):
        course = Course.objects.create(title="Django", description="Web framework")
        course.teachers.add(self.teacher)

        url = reverse('courses-detail', args=[course.id])
        response = self.client.get(url, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Django")
        self.assertEqual(response.data['description'], "Web framework")

    def test_update_course(self):
        course = Course.objects.create(title="Old Title", description="Old Description")
        course.teachers.add(self.teacher)

        url = reverse('courses-detail', args=[course.id])
        data = {"title": "Updated Title", "description": "Updated Description"}
        response = self.client.put(url, data, format='json', **self.get_auth_headers(self.teacher_token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        course.refresh_from_db()
        self.assertEqual(course.title, "Updated Title")
        self.assertEqual(course.description, "Updated Description")

    def test_delete_course(self):
        course = Course.objects.create(title="To Delete", description="Will be deleted")
        course.teachers.add(self.teacher)

        url = reverse('courses-detail', args=[course.id])
        response = self.client.delete(url, **self.get_auth_headers(self.teacher_token))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

    def test_course_creation_with_missing_title(self):
        url = reverse('courses-list')
        data = {"description": "Missing title"}  # Нет title
        response = self.client.post(url, data, format='json', **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Course.objects.count(), 0)

    def test_course_creation_with_long_title(self):
        url = reverse('courses-list')
        data = {"title": "A" * 256, "description": "Title too long"}
        response = self.client.post(url, data, format='json', **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Course.objects.count(), 0)
