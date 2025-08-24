from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status

register_user_docs = extend_schema(
    tags=["Users"],
    summary="New user registration",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "email": {"type": "string"},
                "password": {"type": "string"},
                "role": {"type": "string", "enum": ["student", "teacher", "admin"]},
            },
            "required": ["username", "password"],
        }
    },
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(description="User created"),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Ошибка валидации"),
    },
)

user_list_docs = extend_schema(
    tags=["Users"],
    summary="Validation error",
)
