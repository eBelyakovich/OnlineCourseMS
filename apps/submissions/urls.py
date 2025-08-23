from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubmissionViewSet, GradeViewSet, GradeCommentViewSet

router = DefaultRouter()
router.register(r'submissions', SubmissionViewSet, basename='submissions')
router.register(r'grades', GradeViewSet, basename='grades')
router.register(r'comments', GradeCommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]
