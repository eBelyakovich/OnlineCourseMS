from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LectureViewSet, HomeworkViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lectures', LectureViewSet, basename='lectures')
router.register(r'homeworks', HomeworkViewSet, basename='homeworks')

urlpatterns = [
    path('', include(router.urls)),
]
