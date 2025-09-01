from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.courses.docs.course_docs import add_student_docs, remove_student_docs, add_teacher_docs, course_create_docs, \
    course_update_docs, course_destroy_docs
from apps.courses.docs.homework_docs import homework_create_docs, homework_update_docs, homework_destroy_docs
from apps.courses.docs.lectures_docs import lecture_create_docs, lecture_update_docs, lecture_destroy_docs
from apps.courses.models import Course, Lecture, Homework
from apps.courses.permissions import IsTeacher
from apps.courses.serializers import CourseSerializer, LectureSerializer, HomeworkSerializer
from apps.courses.services.course_service import CourseService
from apps.courses.services.homework_service import HomeworkService
from apps.courses.services.lecture_service import LectureService


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.teachers.add(self.request.user)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "add_student", "add_teacher"]:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    @add_student_docs
    @action(detail=True, methods=['post'], permission_classes=[IsTeacher])
    def add_student(self, request, pk=None):
        course = self.get_object()
        data, status_code = CourseService.add_student(course, request.data.get('student_id'))
        return Response(data, status=status_code)

    @remove_student_docs
    @action(detail=True, methods=['post'], permission_classes=[IsTeacher])
    def remove_student(self, request, pk=None):
        course = self.get_object()
        data, status_code = CourseService.remove_student(course, request.data.get('student_id'))
        return Response(data, status=status_code)

    @add_teacher_docs
    @action(detail=True, methods=["post"], permission_classes=[IsTeacher])
    def add_teacher(self, request, pk=None):
        course = self.get_object()
        data, status_code = CourseService.add_teacher(course, request.data.get('teacher_id'))
        return Response(data,status=status_code)

    @course_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @course_update_docs
    def update(self, request, *args, **kwargs):
        course = self.get_object()
        CourseService.check_edit_permissions(course, request.user)
        return super().update(request, *args, **kwargs)

    @course_destroy_docs
    def destroy(self, request, *args, **kwargs):
        course = self.get_object()
        CourseService.check_edit_permissions(course, request.user)
        return super().destroy(request, *args, **kwargs)


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        LectureService.check_create_permissions(course, self.request.user)
        serializer.save()

    @lecture_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @lecture_update_docs
    def update(self, request, *args, **kwargs):
        lecture = self.get_object()
        LectureService.check_edit_permissions(lecture, request.user)
        return super().update(request, *args, **kwargs)

    @lecture_destroy_docs
    def destroy(self, request, *args, **kwargs):
        lecture = self.get_object()
        LectureService.check_edit_permissions(lecture, request.user)
        return super().destroy(request, *args, **kwargs)


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        lecture = serializer.validated_data['lecture']
        HomeworkService.check_create_permissions(lecture, self.request.user)
        serializer.save()

    @homework_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @homework_update_docs
    def update(self, request, *args, **kwargs):
        homework = self.get_object()
        HomeworkService.check_edit_permissions(homework, request.user)
        return super().update(request, *args, **kwargs)

    @homework_destroy_docs
    def destroy(self, request, *args, **kwargs):
        homework = self.get_object()
        HomeworkService.check_edit_permissions(homework, request.user)
        return super().destroy(request, *args, **kwargs)
