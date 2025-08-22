from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from course.models import User, Course, Lecture, Homework, Submission, Grade, GradeComment


class GradeCommentTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="123", role="teacher")
        self.student = User.objects.create_user(username="student", password="123", role="student")

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
            grade="A",
            comment="Nice work"
        )

    def test_student_add_comment(self):
        self.client.login(username="student", password="123")
        url = reverse("gradecomment-list")
        data = {"grade": self.grade.id, "text": "Спасибо за проверку!"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GradeComment.objects.count(), 1)
        self.assertEqual(GradeComment.objects.first().text, "Спасибо за проверку!")

    def test_teacher_add_comment(self):
        self.client.login(username="teacher", password="123")
        url = reverse("gradecomment-list")
        data = {"grade": self.grade.id, "text": "Следующий раз попробуй оптимизировать код"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GradeComment.objects.count(), 1)

    def test_student_cannot_comment_other_students_grade(self):
        other_student = User.objects.create_user(username="kate", password="123", role="student")
        other_submission = Submission.objects.create(homework=self.homework, student=other_student, answer_text="Other")
        other_grade = Grade.objects.create(submission=other_submission, teacher=self.teacher, grade="B")

        self.client.login(username="student", password="123")
        url = reverse("gradecomment-list")
        data = {"grade": other_grade.id, "text": "Я тут случайно..."}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(GradeComment.objects.count(), 0)
