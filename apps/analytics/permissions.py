from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Разрешение для доступа только аутентифицированным пользователям.
    Неаутентифицированные пользователи могут только читать данные.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешение на доступ только для владельца объекта.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user