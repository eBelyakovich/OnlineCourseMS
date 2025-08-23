from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == 'admin'
