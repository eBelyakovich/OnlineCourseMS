from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from course.models import User, Course, Lecture, Homework, Submission, Grade


class PermissionTests(APITestCase):
    def setUp(self):
        self.teacher1 = User.objects.create_user(username="teacher1", password="123", role="teacher")
        self.teacher2 = User.objects.create_user(username="teacher2", password="123", role="teacher")
        self.student = User.objects.create_user(username="student", password="123", role="student")

        self.course = Course.objects.create(title="Python", description="Learn Python")
        self.course.teachers.add(self.teacher1)

    def test_student_cannot_create_course(self):
        self.client.login(username="student", password="123")
        url = reverse("course-list")
        data = {"title": "HackCourse", "description": "Should not work"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_create_course(self):
        self.client.login(username="teacher1", password="123")
        url = reverse("course-list")
        data = {"title": "Django", "description": "Web framework"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_cannot_edit_other_teacher_course(self):
        self.client.login(username="teacher2", password="123")
        url = reverse("course-detail", args=[self.course.id])
        data = {"title": "Hacked course"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_create_lecture(self):
        self.client.login(username="student", password="123")
        url = reverse("lecture-list")
        data = {"course": self.course.id, "topic": "Hack lecture"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_grade_submission(self):
        lecture = Lecture.objects.create(course=self.course, topic="Lesson 1")
        hw = Homework.objects.create(lecture=lecture, text="Task 1")
        sub = Submission.objects.create(homework=hw, student=self.student, answer_text="My answer")

        self.client.login(username="student", password="123")
        url = reverse("grade-list")
        data = {"submission": sub.id, "grade": "A", "comment": "Self grade"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_grade_submission(self):
        lecture = Lecture.objects.create(course=self.course, topic="Lesson 1")
        hw = Homework.objects.create(lecture=lecture, text="Task 1")
        sub = Submission.objects.create(homework=hw, student=self.student, answer_text="My answer")

        self.client.login(username="teacher1", password="123")
        url = reverse("grade-list")
        data = {"submission": sub.id, "grade": "B", "comment": "Ok"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Grade.objects.count(), 1)
