from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from apps.courses.permissions import IsOwner, IsStudent, IsTeacher
from apps.submissions.docs.grades_docs import grade_create_docs, grade_update_docs, grade_destroy_docs, \
    comment_create_docs
from apps.submissions.docs.submission_docs import submission_create_docs, submission_update_docs
from apps.submissions.models import Submission, Grade, GradeComment
from apps.submissions.serializers import GradeCommentSerializer, SubmissionSerializer, GradeSerializer
from apps.users.models import User


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

    @submission_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @submission_update_docs
    def update(self, request, *args, **kwargs):
        submission = self.get_object()
        user = request.user
        if not (user.is_superuser or submission.student == user):
            raise PermissionDenied("You cannot edit another student's submission.")
        return super().update(request, *args, **kwargs)

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

    @grade_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @grade_update_docs
    def update(self, request, *args, **kwargs):
        grade = self.get_object()
        user = request.user
        if not (user.is_superuser or grade.teacher == user):
            raise PermissionDenied("You cannot edit another teacher's grade.")
        return super().update(request, *args, **kwargs)

    @grade_destroy_docs
    def destroy(self, request, *args, **kwargs):
        grade = self.get_object()
        user = request.user
        if not (user.is_superuser or grade.teacher == user):
            raise PermissionDenied("You cannot delete another teacher's grade.")
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


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

    @comment_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
