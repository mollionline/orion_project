from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from rest_framework.response import Response

from .serializers import UserSigninSerializer, UserSerializer
from .authentication import token_expire_handler, expires_in


# Create your views here.

class UserPermission(permissions.BasePermission):
    message = 'У вас нет прав доступа!'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.user == request.user.is_staff:
            return True
        return False


class LogoutView(APIView):
    """Логоут"""
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})


class SignInAPIView(GenericAPIView):
    """Логин"""
    permission_classes = [AllowAny]
    serializer_class = UserSigninSerializer

    def post(self, request, *args, **kwargs):
        signin_serializer = UserSigninSerializer(data=request.data)
        if not signin_serializer.is_valid():
            return Response(signin_serializer.errors, status=HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=signin_serializer.data['username'],
            password=signin_serializer.data['password']
        )
        if not user:
            return Response({'detail': 'Неверные учетные данные или активируйте учетную запись'}, status=HTTP_404_NOT_FOUND)

        # TOKEN STUFF
        token, _ = Token.objects.get_or_create(user=user)

        # token_expire_handler  проверяет срок токена, если срок токена истек то удаляет его
        is_expired, token = token_expire_handler(token)
        user_serialized = UserSerializer(user)

        return Response({
            'user': user_serialized.data,
            'expires_in': expires_in(token),
            'token': token.key
        }, status=HTTP_200_OK)


@api_view(["GET"])
def user_info(request):
    return Response({
        'user': request.user.username,
        'expires_in': f"{expires_in(request.auth)} секунд"
    }, status=HTTP_200_OK)