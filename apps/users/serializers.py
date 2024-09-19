from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.users.models import User
from django.contrib.auth import authenticate


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'position']

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Пароль должен содержать минимум 8 символов.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            position=validated_data.get('position', 'TENANT')
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        # Получаем email и пароль из запроса
        email = attrs.get('email')
        password = attrs.get('password')

        # Аутентифицируем пользователя
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError({"detail": "Пользователь с такими данными не найден или пароль неверный."})

        # Присваиваем email в поле 'username' для дальнейшей работы JWT
        attrs['username'] = user.email

        # Передаём валидацию в родительский класс для создания токенов
        return super().validate(attrs)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'position']