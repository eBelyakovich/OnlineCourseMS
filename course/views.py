from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from course.models import User, Course, Lecture, Homework, Submission, Grade
from course.permissions import IsTeacher, IsStudent, IsOwner
from course.serializers import UserSerializer, CourseSerializer, LectureSerializer, HomeworkSerializer, \
    SubmissionSerializer, GradeSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "add_student", "add_teacher"]:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'], permission_classes=[IsTeacher])
    def add_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        try:
            student = User.objects.get(id=student_id, role='student')
            course.students.add(student)
            return Response({'status': 'student added'})
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=400)

    @action(detail=True, methods=["post"], permission_classes=[IsTeacher])
    def add_teacher(self, request, pk=None):
        course = self.get_object()
        teacher_id = request.data.get('teacher_id')
        try:
            teacher = User.objects.get(id=teacher_id, role='teacher')
            course.teachers.add(teacher)
            return Response({'status': 'teacher added'})
        except User.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=400)


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsStudent()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsOwner()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(password=make_password(serializer.validated_data['password']))
