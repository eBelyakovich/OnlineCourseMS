from django.db import models

from apps.courses.models import Homework
from apps.users.models import User


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
