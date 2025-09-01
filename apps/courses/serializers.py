from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.courses.models import Course, Lecture, Homework
from apps.users.serializers import UserSerializer


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
