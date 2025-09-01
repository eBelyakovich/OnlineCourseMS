from rest_framework.exceptions import PermissionDenied
from apps.submissions.models import Submission
from apps.users.models import User


class SubmissionService:
    @staticmethod
    def get_queryset_for_user(user: User):
        return Submission.objects.for_user(user)

    @staticmethod
    def check_edit_permissions(submission: Submission, user: User):
        if not (user.is_superuser or submission.student == user):
            raise PermissionDenied("You cannot edit another student's submission.")

    @staticmethod
    def check_create_permissions(homework, user):
        if user.role != user.Role.STUDENT:
            raise PermissionDenied("Only students can submit homework.")
