from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import QuerySet

from apps.courses.models import Homework
from apps.submissions.constants import GRADE_MIN, GRADE_MAX
from apps.users.models import User


class SubmissionQuerySet(QuerySet):
    def for_user(self, user):
        if user.is_superuser:
            return self.all()
        if user.role == user.Role.STUDENT:
            return self.filter(student=user)
        if user.role == user.Role.TEACHER:
            return self.filter(homework__lecture__course__teachers=user)
        return self.none()


class SubmissionManager(models.Manager):
    def get_queryset(self):
        return SubmissionQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user)


class GradeQuerySet(QuerySet):
    def for_user(self, user):
        if user.is_superuser:
            return self.all()
        if user.role == user.Role.STUDENT:
            return self.filter(submission__student=user)
        if user.role == user.Role.TEACHER:
            return self.filter(submission__homework__lecture__course__teachers=user)
        return self.none()


class GradeManager(models.Manager):
    def get_queryset(self):
        return GradeQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user)


class GradeCommentQuerySet(QuerySet):
    def for_user(self, user):
        if user.is_superuser:
            return self.all()
        if user.role == user.Role.STUDENT:
            return self.filter(grade__submission__student=user)
        if user.role == user.Role.TEACHER:
            return self.filter(grade__submission__homework__lecture__course__teachers=user)
        return self.none()


class GradeCommentManager(models.Manager):
    def get_queryset(self):
        return GradeCommentQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user)


class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    answer_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    objects = SubmissionManager()


class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    teacher = models.ForeignKey('users.User', on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(GRADE_MIN), MaxValueValidator(GRADE_MAX)])
    comment = models.TextField(blank=True, null=True)

    objects = GradeManager()

    def __str__(self):
        return f'Grade {self.grade} for {self.submission.student.username}'


class GradeComment(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = GradeCommentManager()

    def __str__(self):
        return f'Comment by {self.author.username} on grade {self.grade.id}'
