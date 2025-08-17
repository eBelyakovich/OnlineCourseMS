from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        TEACHER = 'teacher', 'Teacher'
        STUDENT = 'student', 'Student'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )

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
