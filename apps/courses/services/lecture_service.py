from rest_framework.exceptions import PermissionDenied
from apps.courses.models import Lecture
from apps.users.models import User


class LectureService:
    @staticmethod
    def check_edit_permissions(lecture: Lecture, user: User):
        if not (user.is_superuser or lecture.course.teachers.filter(id=user.id).exists()):
            raise PermissionDenied("You cannot modify another teacher's lecture.")

    @staticmethod
    def check_create_permissions(course, user):
        if not (user.is_superuser or user in course.teachers.all()):
            raise PermissionDenied("You are not a teacher of this course")