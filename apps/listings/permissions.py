from rest_framework import permissions

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Права доступа разрешают просмотр для всех пользователей, а запись только аутентифицированным пользователям.
    """
    def has_permission(self, request, view):
        # Разрешаем просмотр для всех пользователей, а запись — только для аутентифицированных
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


