import json

from django.core import serializers
from django.http import Http404, JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import permissions, generics, filters
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from rest_framework.response import Response

from .serializers import UserSigninSerializer, UserSerializer, NodeSerializer
from .authentication import token_expire_handler, expires_in
from .models import Apartment, House, Node


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
            return Response({'detail': 'Неверные учетные данные или активируйте учетную запись'},
                            status=HTTP_404_NOT_FOUND)

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


class CreateNodeAPIView(generics.GenericAPIView):
    """Создать узел в привязке к квартире"""
    permission_classes = [IsAuthenticated]
    serializer_class = NodeSerializer

    def get_queryset(self):
        return Apartment.objects.all()

    def get_object(self, pk):
        try:
            return Apartment.objects.get(pk=pk)
        except Apartment.DoesNotExist:
            raise Http404

    def post(self, request, pk, *args, **kwargs):
        apartment = self.get_object(pk)
        data = json.loads(request.body)
        serializer = NodeSerializer(data=data)
        if not apartment.node_id:
            if serializer.is_valid():
                serializer.save()
                apartment.node_id = serializer.data.get('uuid')
                apartment.save()
                return JsonResponse(serializer.data, safe=False)
            else:
                response = JsonResponse({'errors': serializer.errors})
                response.status_code = 400
                return response
        else:
            response = JsonResponse({'errors': 'Ошибка, у квартиры уже есть узел'})
            response.status_code = 400
            return response


class UpdateNodeAPIView(generics.GenericAPIView):
    """Редактировать узел по uuid"""
    permission_classes = [IsAuthenticated]
    serializer_class = NodeSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Node.objects.all()

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = json.loads(request.body)
        serializer = NodeSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            response = JsonResponse({'errors': serializer.errors})
            response.status_code = 400
            return response


class NodesListAPIView(generics.ListAPIView):
    """Список узлов и фильтрация по приведенным полям"""
    serializer_class = NodeSerializer
    queryset = Node.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['description', 'name', 'address', 'owner', 'uuid']
