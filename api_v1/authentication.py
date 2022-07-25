from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from datetime import timedelta
from django.utils import timezone


# ставит время жизни 7 дней и отправляет время жизни token-a
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(hours=168) - time_elapsed
    return left_time


# проверяет  token
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


# проверяет время жизни token-a
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
    return is_expired, token


class ExpiringTokenAuthentication(TokenAuthentication):
    """Если у token-а истекает срок то он удаляется"""

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Не правильный token")

        if not token.user.is_active:
            raise AuthenticationFailed("Пользователь не активен")

        is_expired, token = token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed("Время token-a истек")

        return (token.user, token)
