from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from course.models import User, Course, Lecture, Homework, Submission, Grade, GradeComment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "role")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    teachers = UserSerializer(many=True, read_only=True)
    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teachers', 'students']


class LectureSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Lecture
        fields = ['id', 'course', 'topic', 'presentation']


class HomeworkSerializer(serializers.ModelSerializer):
    lecture = serializers.PrimaryKeyRelatedField(queryset=Lecture.objects.all())

    class Meta:
        model = Homework
        fields = ['id', 'lecture', 'text']


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


class GradeCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = GradeComment
        fields = ['id', 'grade', 'author', 'text', 'created_at']
