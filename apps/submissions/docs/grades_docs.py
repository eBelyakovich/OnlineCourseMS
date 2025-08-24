from drf_spectacular.utils import extend_schema
from rest_framework import status

grade_create_docs = extend_schema(
    tags=["Grades"],
    summary="Выставить оценку",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "submission": {"type": "integer"},
                "teacher": {"type": "integer"},
                "grade": {"type": "integer"},
                "comment": {"type": "string"},
            },
            "required": ["submission", "teacher", "grade"],
        }
    },
    responses={status.HTTP_201_CREATED: {"id": {"type": "integer"}}},
)

grade_update_docs = extend_schema(
    tags=["Grades"],
    summary="Обновить оценку",
)

grade_destroy_docs = extend_schema(
    tags=["Grades"],
    summary="Удалить оценку",
)

comment_create_docs = extend_schema(
    tags=["Comments"],
    summary="Добавить комментарий к оценке",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "grade": {"type": "integer"},
                "text": {"type": "string"},
            },
            "required": ["grade", "text"],
        }
    },
    responses={status.HTTP_201_CREATED: {"id": {"type": "integer"}}},
)
