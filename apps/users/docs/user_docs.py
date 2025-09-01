from drf_spectacular.utils import extend_schema, OpenApiResponse
from apps.users.serializers import (
    LoginSerializer,
    LogoutSerializer,
    UserSerializer,
)


login_docs = extend_schema(
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            response={"type": "object", "properties": {"message": {"type": "string"}}},
            description="Login successful",
        ),
        400: OpenApiResponse(description="Invalid credentials"),
    },
    description="Authenticate user and start a session.",
)


logout_docs = extend_schema(
    request=LogoutSerializer,
    responses={
        200: OpenApiResponse(
            response={"type": "object", "properties": {"detail": {"type": "string"}}},
            description="Logout successful",
        )
    },
    description="Log out current user and end session.",
)


me_docs = extend_schema(
    responses=UserSerializer,
    description="Get information about the currently authenticated user.",
)


register_user_docs = extend_schema(
    request=UserSerializer,
    responses={
        201: UserSerializer,
        400: OpenApiResponse(description="Invalid input data"),
    },
    description="Register a new user (Student or Teacher).",
)
