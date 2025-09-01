from rest_framework.exceptions import PermissionDenied
from apps.users.models import User
from apps.courses.models import Course


class CourseService:
    @staticmethod
    def add_student(course: Course, student_id: int):
        try:
            student = User.objects.get(id=student_id, role=User.Role.STUDENT)
            course.students.add(student)
            return {"status": "student added"}, 200
        except User.DoesNotExist:
            return {"error": "Student not found"}, 400

    @staticmethod
    def remove_student(course: Course, student_id: int):
        try:
            student = User.objects.get(id=student_id, role=User.Role.STUDENT)
            course.students.remove(student)
            return {"status": f"Student {student.username} removed"}, 200
        except User.DoesNotExist:
            return {"error": "Student not found"}, 400

    @staticmethod
    def add_teacher(course: Course, teacher_id: int):
        try:
            teacher = User.objects.get(id=teacher_id, role=User.Role.TEACHER)
            course.teachers.add(teacher)
            return {"status": "teacher added"}, 200
        except User.DoesNotExist:
            return {"error": "Teacher not found"}, 400

    @staticmethod
    def check_edit_permissions(course: Course, user: User):
        if not (user.is_superuser or course.teachers.filter(id=user.id).exists()):
            raise PermissionDenied("You cannot modify another teacher's course.")
