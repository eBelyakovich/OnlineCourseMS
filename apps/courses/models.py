from django.db import models
from django.db.models import QuerySet

from apps.users.models import User


class CourseQuerySet(QuerySet):
    def for_user(self, user):
        if user.is_superuser:
            return self.all()
        if user.role == user.Role.STUDENT:
            return self.filter(students=user)
        if user.role == user.Role.TEACHER:
            return self.filter(teachers=user)
        return self.none()

    def with_teacher(self):
        return self.prefetch_related('teachers')

    def available(self):
        return self.filter(is_active=True)


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def with_teacher(self):
        return self.get_queryset().with_teacher()

    def available(self):
        return self.get_queryset().available()


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    teachers = models.ManyToManyField('users.User', related_name='teaching_courses')
    students = models.ManyToManyField('users.User', related_name='enrolled_courses')

    objects = CourseManager()

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
