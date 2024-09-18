from rest_framework import permissions

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешает просмотр данных для всех пользователей, а изменение — только для аутентифицированных пользователей.
    """
    def has_permission(self, request, view):
        # Если запрос является "безопасным" (т.е. только чтение), разрешаем всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Иначе разрешаем только аутентифицированным пользователям
        return request.user and request.user.is_authenticated