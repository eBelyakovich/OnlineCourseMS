from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status

lecture_create_docs = extend_schema(
    tags=["Lectures"],
    summary="Create a lecture",
    responses={status.HTTP_201_CREATED: OpenApiResponse(description="Lecture created")},
)

lecture_update_docs = extend_schema(
    tags=["Lectures"],
    summary="Update lecture",
)

lecture_destroy_docs = extend_schema(
    tags=["Lectures"],
    summary="Delete lecture",
)
