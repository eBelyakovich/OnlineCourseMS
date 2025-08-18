from rest_framework import serializers

from course.models import User, Course, Lecture, Homework, Submission, Grade


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        extra_kwargs = {'password': {'write_only': True}}


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
