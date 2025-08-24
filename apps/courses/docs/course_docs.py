from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import status

course_create_docs = extend_schema(
    tags=["Courses"],
    summary="Create a course",
    responses={status.HTTP_201_CREATED: OpenApiResponse(description="Course created")},
)

course_update_docs = extend_schema(
    tags=["Courses"],
    summary="Update course",
    responses={status.HTTP_200_OK: OpenApiResponse(description="Course updated")},
)

course_destroy_docs = extend_schema(
    tags=["Courses"],
    summary="Delete course",
    responses={status.HTTP_204_NO_CONTENT: OpenApiResponse(description="Course deleted")},
)

add_student_docs = extend_schema(
    tags=["Courses"],
    summary="Add a student to a course",
    parameters=[
        OpenApiParameter("student_id", type=int, required=True, location=OpenApiParameter.QUERY),
    ],
)

remove_student_docs = extend_schema(
    tags=["Courses"],
    summary="Remove student from course",
    parameters=[
        OpenApiParameter("student_id", type=int, required=True, location=OpenApiParameter.QUERY),
    ],
)

add_teacher_docs = extend_schema(
    tags=["Courses"],
    summary="Add a teacher to a course",
    parameters=[
        OpenApiParameter("teacher_id", type=int, required=True, location=OpenApiParameter.QUERY),
    ],
)
