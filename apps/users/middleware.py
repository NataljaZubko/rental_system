from datetime import datetime, timezone
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Получаем токены из cookies
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        # Проверяем access_token
        if access_token:
            try:
                token = AccessToken(access_token)
                if datetime.fromtimestamp(token['exp'], tz=timezone.utc) < datetime.now(tz=timezone.utc):
                    raise TokenError('Token expired')
                # Добавляем токен в заголовки запроса
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
            except TokenError:
                # Если токен истек, обновляем его через refresh_token
                new_access_token = self.refresh_access_token(refresh_token)
                if new_access_token:
                    request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                    request._new_access_token = new_access_token
                else:
                    self.clear_cookies(request)
        elif refresh_token:
            # Если access_token отсутствует, проверяем refresh_token и обновляем access_token
            new_access_token = self.refresh_access_token(refresh_token)
            if new_access_token:
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                request._new_access_token = new_access_token
            else:
                self.clear_cookies(request)

    def refresh_access_token(self, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return new_access_token
        except TokenError:
            return None

    def process_response(self, request, response):
        new_access_token = getattr(request, '_new_access_token', None)
        if new_access_token:
            # Обновляем access_token в cookies
            access_expiry = AccessToken(new_access_token)['exp']
            response.set_cookie(
                key='access_token',
                value=new_access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=datetime.fromtimestamp(access_expiry, tz=timezone.utc)
            )
        return response

    def clear_cookies(self, request):
        request.COOKIES.pop('access_token', None)
        request.COOKIES.pop('refresh_token', None)