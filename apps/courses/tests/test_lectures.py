from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from apps.courses.models import Course, Lecture
from apps.users.models import User


class LectureTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="123", role="teacher")
        self.student = User.objects.create_user(username="student", password="123", role="student")
        self.other_teacher = User.objects.create_user(username="other_teacher", password="123", role="teacher")

        self.teacher_token = str(AccessToken.for_user(self.teacher))
        self.student_token = str(AccessToken.for_user(self.student))
        self.other_teacher_token = str(AccessToken.for_user(self.other_teacher))

        self.course = Course.objects.create(title="Python", description="Learn Python")
        self.course.teachers.add(self.teacher)

    def get_auth_headers(self, token):
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    def test_teacher_can_add_lecture(self):
        url = reverse('lectures-list')
        data = {"course": self.course.id, "topic": "Intro"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lecture.objects.count(), 1)
        self.assertEqual(Lecture.objects.first().topic, "Intro")
        self.assertEqual(Lecture.objects.first().course, self.course)

    def test_student_cannot_add_lecture(self):
        url = reverse('lectures-list')
        data = {"course": self.course.id, "topic": "Student Lecture"}
        response = self.client.post(url, data, **self.get_auth_headers(self.student_token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lecture.objects.count(), 0)

    def test_teacher_cannot_add_lecture_to_other_teacher_course(self):
        other_course = Course.objects.create(title="Other Course", description="Other teacher's course")
        other_course.teachers.add(self.other_teacher)

        url = reverse('lectures-list')
        data = {"course": other_course.id, "topic": "Unauthorized Lecture"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lecture.objects.count(), 0)

    def test_unauthenticated_user_cannot_add_lecture(self):
        url = reverse('lectures-list')
        data = {"course": self.course.id, "topic": "Anonymous Lecture"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Lecture.objects.count(), 0)

    def test_add_lecture_with_missing_topic(self):
        url = reverse('lectures-list')
        data = {"course": self.course.id}  # Нет topic
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lecture.objects.count(), 0)

    def test_add_lecture_with_missing_course(self):
        url = reverse('lectures-list')
        data = {"topic": "Lecture without course"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lecture.objects.count(), 0)

    def test_add_lecture_with_nonexistent_course(self):
        url = reverse('lectures-list')
        data = {"course": 999, "topic": "Lecture for non-existent course"}
        response = self.client.post(url, data, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lecture.objects.count(), 0)

    def test_get_lectures_list(self):
        Lecture.objects.create(course=self.course, topic="Lecture 1")
        Lecture.objects.create(course=self.course, topic="Lecture 2")

        url = reverse('lectures-list')
        response = self.client.get(url, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_lecture_detail(self):
        lecture = Lecture.objects.create(course=self.course, topic="Detailed Lecture")

        url = reverse('lectures-detail', args=[lecture.id])
        response = self.client.get(url, **self.get_auth_headers(self.teacher_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['topic'], "Detailed Lecture")
        self.assertEqual(response.data['course'], self.course.id)

    def test_update_lecture(self):
        lecture = Lecture.objects.create(course=self.course, topic="Old Topic")

        url = reverse('lectures-detail', args=[lecture.id])
        data = {"topic": "Updated Topic"}
        response = self.client.patch(url, data, **self.get_auth_headers(self.teacher_token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        lecture.refresh_from_db()
        self.assertEqual(lecture.topic, "Updated Topic")

    def test_delete_lecture(self):
        lecture = Lecture.objects.create(course=self.course, topic="To Delete")

        url = reverse('lectures-detail', args=[lecture.id])
        response = self.client.delete(url, **self.get_auth_headers(self.teacher_token))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lecture.objects.count(), 0)
