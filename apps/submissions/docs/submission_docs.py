from drf_spectacular.utils import extend_schema
from rest_framework import status

submission_create_docs = extend_schema(
    tags=["Submissions"],
    summary="Отправить решение",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "homework": {"type": "integer"},
                "student": {"type": "integer"},
                "answer": {"type": "string"},
            },
            "required": ["homework", "student", "answer"],
        }
    },
    responses={status.HTTP_201_CREATED: {"id": {"type": "integer"}}},
)

submission_update_docs = extend_schema(
    tags=["Submissions"],
    summary="Обновить решение студента",
)
