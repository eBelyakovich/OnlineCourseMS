from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

# Documentation for main actions
course_list_docs = swagger_auto_schema(
    operation_summary="Get all courses",
    operation_description="""
    Returns a list of all available courses.
    For authenticated users only.
    """,
    responses={
        200: "CourseSerializer(many=True)",
        401: "Unauthorized",
    }
)

course_create_docs = swagger_auto_schema(
    operation_summary="Create new course",
    operation_description="""
    Create a new course. Only for users with TEACHER role.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['title'],
        properties={
            'title': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Course title (max 255 characters)",
                maxLength=255
            ),
            'description': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Course description"
            ),
        }
    ),
    responses={
        201: "CourseSerializer",
        400: "Invalid data (e.g., missing title)",
        403: "Only TEACHER can create courses"
    }
)

course_retrieve_docs = swagger_auto_schema(
    operation_summary="Get course details",
    operation_description="""
    Returns detailed information about a specific course.
    For authenticated users only.
    """,
    responses={
        200: "CourseSerializer",
        404: "Course not found"
    }
)

course_update_docs = swagger_auto_schema(
    operation_summary="Full course update",
    operation_description="""
    Full update of course information. Only for TEACHER of this course.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['title'],
        properties={
            'title': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Course title (max 255 characters)",
                maxLength=255
            ),
            'description': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Course description"
            ),
        }
    ),
    responses={
        200: "CourseSerializer",
        400: "Invalid data",
        403: "Only TEACHER of this course can update it",
        404: "Course not found"
    }
)

course_partial_update_docs = swagger_auto_schema(
    operation_summary="Partial course update",
    operation_description="""
    Partial update of course information. Only for TEACHER of this course.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Course title (max 255 characters)",
                maxLength=255
            ),
            'description': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Course description"
            ),
        }
    ),
    responses={
        200: "CourseSerializer",
        400: "Invalid data",
        403: "Only TEACHER of this course can update it",
        404: "Course not found"
    }
)

course_destroy_docs = swagger_auto_schema(
    operation_summary="Delete course",
    operation_description="""
    Delete a course. Only for TEACHER of this course.
    """,
    responses={
        204: "Course deleted successfully",
        403: "Only TEACHER of this course can delete it",
        404: "Course not found"
    }
)

# Documentation for custom actions
add_student_docs = swagger_auto_schema(
    operation_summary="Add student to course",
    operation_description="""
    Add a student to the course. Only for TEACHER of this course.
    The user must have STUDENT role.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['student_id'],
        properties={
            'student_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="ID of the student user"
            )
        }
    ),
    responses={
        200: openapi.Response(
            description="Student added successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Success message"
                    )
                }
            )
        ),
        400: openapi.Response(
            description="Error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Error message"
                    )
                }
            )
        ),
        403: "Only TEACHER of this course can add students",
        404: "Course or student not found"
    }
)

remove_student_docs = swagger_auto_schema(
    operation_summary="Remove student from course",
    operation_description="""
    Remove a student from the course. Only for TEACHER of this course.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['student_id'],
        properties={
            'student_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="ID of the student user"
            )
        }
    ),
    responses={
        200: openapi.Response(
            description="Student removed successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Success message"
                    )
                }
            )
        ),
        400: openapi.Response(
            description="Error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Error message"
                    )
                }
            )
        ),
        403: "Only TEACHER of this course can remove students",
        404: "Course or student not found"
    }
)

add_teacher_docs = swagger_auto_schema(
    operation_summary="Add teacher to course",
    operation_description="""
    Add a teacher to the course. Only for TEACHER of this course.
    The user must have TEACHER role.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['teacher_id'],
        properties={
            'teacher_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="ID of the teacher user"
            )
        }
    ),
    responses={
        200: openapi.Response(
            description="Teacher added successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Success message"
                    )
                }
            )
        ),
        400: openapi.Response(
            description="Error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Error message"
                    )
                }
            )
        ),
        403: "Only TEACHER of this course can add teachers",
        404: "Course or teacher not found"
    }
)