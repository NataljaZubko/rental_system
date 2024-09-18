# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import RegisterUserSerializer, UserListSerializer, CustomTokenObtainPairSerializer
# from apps.users.models import User
#
# class UserRegisterView(generics.CreateAPIView):
#     """
#     Регистрация нового пользователя. Возвращает токены и информацию о пользователе.
#     """
#     serializer_class = RegisterUserSerializer
#     permission_classes = [permissions.AllowAny]  # Разрешает доступ к регистрации без аутентификации
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#
#         # Создание токенов
#         refresh = RefreshToken.for_user(user)
#         access_token = refresh.access_token
#
#         # Формирование ответа с токенами
#         response = Response({
#             'user': {
#                 'first_name': user.first_name,
#                 'last_name': user.last_name,
#                 'email': user.email,
#                 'position': user.position,
#             },
#             'tokens': {
#                 'access': str(access_token),
#                 'refresh': str(refresh),
#             }
#         }, status=status.HTTP_201_CREATED)
#
#         # Установка токенов в куки
#         response.set_cookie('access_token', str(access_token), httponly=True, secure=False, samesite='Lax')
#         response.set_cookie('refresh_token', str(refresh), httponly=True, secure=False, samesite='Lax')
#         return response
#
# class UserListView(generics.ListAPIView):
#     """
#     Просмотр списка пользователей. Доступно только для аутентифицированных пользователей.
#     """
#     serializer_class = UserListSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         return User.objects.all()
#
# class LogoutView(APIView):
#     """
#     Выход из системы. Удаляет куки с токенами.
#     """
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         response = Response(status=status.HTTP_204_NO_CONTENT)
#         response.delete_cookie('access_token')
#         response.delete_cookie('refresh_token')
#         return response
#
# class CustomTokenObtainPairView(TokenObtainPairView):
#     """
#     Кастомный эндпоинт для получения токенов с использованием кастомного сериализатора.
#     """
#     serializer_class = CustomTokenObtainPairSerializer

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterUserSerializer, UserListSerializer, CustomTokenObtainPairSerializer
from apps.users.models import User

class UserRegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя. Возвращает информацию о пользователе без токенов.
    """
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]  # Разрешает доступ к регистрации без аутентификации

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Возвращаем информацию о пользователе, но без токенов
        return Response({
            'user': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'position': user.position,
            }
        }, status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    """
    Просмотр списка пользователей. Доступно только для аутентифицированных пользователей.
    """
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()


class LogoutView(APIView):
    """
    Выход из системы. Удаляет куки с токенами.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Кастомный эндпоинт для получения токенов, которые сохраняются в cookies.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        # Сохранение токенов в cookies
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,  # Включить True в продакшене
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=False,  # Включить True в продакшене
            samesite='Lax'
        )

        return response