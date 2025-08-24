from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status

homework_create_docs = extend_schema(
    tags=["Homeworks"],
    summary="Create homework",
    responses={status.HTTP_201_CREATED: OpenApiResponse(description="Homework created")},
)

homework_update_docs = extend_schema(
    tags=["Homeworks"],
    summary="Update homework",
)

homework_destroy_docs = extend_schema(
    tags=["Homeworks"],
    summary="Delete homework",
)
