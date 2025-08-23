from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.courses.models import Course, Lecture, Homework
from apps.courses.permissions import IsTeacher
from apps.courses.serializers import CourseSerializer, LectureSerializer, HomeworkSerializer
from apps.docs.course_docs import *
from apps.users.models import User


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "add_student", "add_teacher"]:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'], permission_classes=[IsTeacher])
    @add_student_docs
    def add_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        try:
            student = User.objects.get(id=student_id, role='student')
            course.students.add(student)
            return Response({'status': 'student added'})
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[IsTeacher])
    @remove_student_docs
    def remove_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        try:
            student = User.objects.get(id=student_id, role='student')
            course.students.remove(student)
            return Response({'status': f'Student {student.username} removed'})
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=400)

    @action(detail=True, methods=["post"], permission_classes=[IsTeacher])
    @add_teacher_docs
    def add_teacher(self, request, pk=None):
        course = self.get_object()
        teacher_id = request.data.get('teacher_id')
        try:
            teacher = User.objects.get(id=teacher_id, role='teacher')
            course.teachers.add(teacher)
            return Response({'status': 'teacher added'})
        except User.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=400)

    @course_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @course_update_docs
    def update(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        if not (user.is_superuser or course.teachers.filter(id=user.id).exists()):
            raise PermissionDenied("You cannot edit another teacher's course.")
        return super().update(request, *args, **kwargs)

    @course_destroy_docs
    def destroy(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        if not (user.is_superuser or course.teachers.filter(id=user.id).exists()):
            raise PermissionDenied("You cannot delete another teacher's course.")
        return super().destroy(request, *args, **kwargs)


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
