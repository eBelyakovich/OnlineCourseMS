from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from apps.courses.permissions import IsOwner, IsStudent, IsTeacher
from apps.submissions.docs.grades_docs import grade_create_docs, grade_update_docs, grade_destroy_docs, \
    comment_create_docs
from apps.submissions.docs.submission_docs import submission_create_docs, submission_update_docs
from apps.submissions.models import Submission, Grade, GradeComment
from apps.submissions.serializers import GradeCommentSerializer, SubmissionSerializer, GradeSerializer
from apps.submissions.services.comment_service import GradeCommentService
from apps.submissions.services.grade_service import GradeService
from apps.submissions.services.submission_service import SubmissionService
from apps.users.models import User


class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        return Submission.objects.for_user(self.request.user)

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
        SubmissionService.check_edit_permissions(submission, request.user)
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer

    def get_queryset(self):
        return Grade.objects.for_user(self.request.user)

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
        GradeService.check_edit_permissions(grade, request.user)
        return super().update(request, *args, **kwargs)

    @grade_destroy_docs
    def destroy(self, request, *args, **kwargs):
        grade = self.get_object()
        GradeService.check_edit_permissions(grade, request.user)
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        submission = serializer.validated_data["submission"]
        GradeService.check_create_permissions(submission, self.request.user)
        serializer.save(teacher=self.request.user)


class GradeCommentViewSet(viewsets.ModelViewSet):
    serializer_class = GradeCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GradeComment.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        grade = serializer.validated_data['grade']
        GradeCommentService.check_edit_permissions(grade, self.request.user)
        serializer.save(author=self.request.user)

    @comment_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
