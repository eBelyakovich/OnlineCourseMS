from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        TEACHER = 'teacher', 'Teacher'
        STUDENT = 'student', 'Student'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True
    )

    objects = UserManager()

    def __str__(self):
        return f'{self.username} ({self.role})'


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


class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    answer_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)


class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='givin_grades',
                                limit_choices_to={'role': User.Role.TEACHER})
    grade = models.IntegerField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Grade {self.grade} for {self.submission.student.username}'


class GradeComment(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grade_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on grade {self.grade.id}'


