from rest_framework import serializers

from apps.courses.models import Homework
from apps.submissions.models import Submission, Grade, GradeComment
from apps.users.serializers import UserSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)  # выставляется автоматически = текущий пользователь
    homework = serializers.PrimaryKeyRelatedField(queryset=Homework.objects.all())

    class Meta:
        model = Submission
        fields = ["id", "homework", "student", "answer_text", "submitted_at"]


class GradeSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)  # текущий юзер = учитель
    submission = serializers.PrimaryKeyRelatedField(queryset=Submission.objects.all())

    class Meta:
        model = Grade
        fields = ["id", "submission", "teacher", "grade", "comment"]

    def validate_grade(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Grade must be between 1 and 5')
        return value


class GradeCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = GradeComment
        fields = ['id', 'grade', 'author', 'text', 'created_at']
