from rest_framework.exceptions import PermissionDenied
from apps.submissions.models import Grade, GradeComment
from apps.users.models import User


class GradeCommentService:
    @staticmethod
    def get_queryset_for_user(user: User):
        return GradeComment.objects.for_user(user)

    @staticmethod
    def check_edit_permissions(grade: Grade, user: User):
        if not (user.is_superuser or grade.teacher == user):
            raise PermissionDenied("You cannot modify another teacher's grade.")

    @staticmethod
    def check_create_permissions(grade, user):
        if user.role == user.Role.STUDENT and grade.submission.student != user:
            raise PermissionDenied("You cannot comment on other students' grades.")

        if user.role == user.Role.TEACHER and not grade.submission.homework.lecture.course.teachers.filter(
                id=user.id).exists():
            raise PermissionDenied("You cannot comment on grades outside your courses.")