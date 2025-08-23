from django.db import models

from apps.users.models import User


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    teachers = models.ManyToManyField(
        User,
        related_name='teaching_courses',
        limit_choices_to={'role': User.Role.TEACHER}
    )
    students = models.ManyToManyField(
        User,
        related_name='enrolled_courses',
        blank=True,
        limit_choices_to={'role': User.Role.STUDENT}
    )

    def __str__(self):
        return self.title


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    topic = models.CharField(max_length=255)
    presentation = models.FileField(upload_to='presentations/', blank=True, null=True)

    def __str__(self):
        return f'{self.course.title}: {self.topic}'


class Homework(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='homeworks')
    text = models.TextField()

    def __str__(self):
        return f'Homework for {self.lecture.topic}'
