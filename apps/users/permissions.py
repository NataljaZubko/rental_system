from rest_framework import permissions

class IsLandlord(permissions.BasePermission):
    """
    Права доступа только для арендодателей (LANDLORD).
    """
    def has_permission(self, request, view):
        # Проверяем, что пользователь авторизован и его позиция 'LANDLORD'
        return request.user and request.user.is_authenticated and request.user.position == 'LANDLORD'


class IsTenant(permissions.BasePermission):
    """
    Права доступа только для арендаторов (TENANT).
    """
    def has_permission(self, request, view):
        # Проверяем, что пользователь авторизован и его позиция 'TENANT'
        return request.user and request.user.is_authenticated and request.user.position == 'TENANT'


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование объявления только его владельцу, остальным пользователям доступен только просмотр.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение доступно всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешение на запись только владельцу объявления
        return obj.owner == request.user