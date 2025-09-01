from rest_framework.exceptions import PermissionDenied
from apps.courses.models import Homework
from apps.users.models import User


class HomeworkService:
    @staticmethod
    def check_edit_permissions(homework: Homework, user: User):
        if not (user.is_superuser or homework.lecture.course.teachers.filter(id=user.id).exists()):
            raise PermissionDenied("You cannot modify another teacher's homework.")
