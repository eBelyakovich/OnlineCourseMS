from rest_framework.exceptions import PermissionDenied
from apps.submissions.models import Grade
from apps.users.models import User


class GradeService:
    @staticmethod
    def get_queryset_for_user(user: User):
        return Grade.objects.for_user(user)

    @staticmethod
    def check_edit_permissions(grade: Grade, user: User):
        if not (user.is_superuser or grade.teacher == user):
            raise PermissionDenied("You cannot modify another teacher's grade.")

    @staticmethod
    def check_create_permissions(submission, user):
        if submission.student == user:
            raise PermissionDenied("You cannot grade your own submission.")