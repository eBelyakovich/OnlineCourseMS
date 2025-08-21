from django.urls import path, include
from rest_framework.routers import DefaultRouter
from course.views import (UserViewSet, CourseViewSet, LectureViewSet,
                          HomeworkViewSet, SubmissionViewSet,
                          GradeViewSet, RegisterView, GradeCommentViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lectures', LectureViewSet, basename='lectures')
router.register(r'homeworks', HomeworkViewSet, basename='homeworks')
router.register(r'submissions', SubmissionViewSet, basename='submissions')
router.register(r'grades', GradeViewSet, basename='grades')
router.register(r'comments', GradeCommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]
