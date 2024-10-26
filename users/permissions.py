from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверка на модератора"""
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


class IsOwner(permissions.BasePermission):
    """Проверка на владельца"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
