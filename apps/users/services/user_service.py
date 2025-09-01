from apps.users.models import User


class UserService:
    @staticmethod
    def create_user(username: str, email: str, password: str, role: str) -> User:
        if role not in [User.Role.STUDENT, User.Role.TEACHER]:
            raise ValueError("Invalid role. Must be 'student' or 'teacher'.")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        return user
