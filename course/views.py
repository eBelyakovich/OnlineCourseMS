from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from course.docs.course_docs import add_student_docs, add_teacher_docs, remove_student_docs, course_create_docs, \
    course_update_docs, course_destroy_docs
from course.models import User, Course, Lecture, Homework, Submission, Grade, GradeComment
from course.permissions import IsTeacher, IsStudent, IsOwner
from course.serializers import UserSerializer, CourseSerializer, LectureSerializer, HomeworkSerializer, \
    SubmissionSerializer, GradeSerializer, GradeCommentSerializer
import course.docs


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)

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


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Submission.objects.all()

        if user.role == User.Role.STUDENT:
            return Submission.objects.filter(student=user)

        if user.role == User.Role.TEACHER:
            return Submission.objects.filter(
                homework__lecture__course__teachers=user
            )
        return Submission.objects.none()

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

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Grade.objects.all()

        if user.role == User.Role.STUDENT:
            return Grade.objects.filter(submission__student=user)

        if user.role == User.Role.TEACHER:
            return Grade.objects.filter(
                submission__homework__lecture__course__teachers=user
            )

        return Grade.objects.none()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class GradeCommentViewSet(viewsets.ModelViewSet):
    queryset = GradeComment.objects.all()
    serializer_class = GradeCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return GradeComment.objects.all()

        if user.role == User.Role.STUDENT:
            return GradeComment.objects.filter(grade__submission__student=user)

        if user.role == User.Role.TEACHER:
            return GradeComment.objects.filter(
                grade__submission__homework__lecture__course__teachers=user
            )
        return GradeComment.objects.none()

    def perform_create(self, serializer):
        grade = serializer.validated_data['grade']
        user = self.request.user

        if user.role == User.Role.STUDENT and grade.submission.student != user:
            raise PermissionDenied("You cannot comment on other students' grades.")

        if user.role == User.Role.TEACHER and not grade.submission.homework.lecture.course.teachers.filter(
                id=user.id).exists():
            raise PermissionDenied("You cannot comment on grades outside your courses.")

        serializer.save(author=user)
