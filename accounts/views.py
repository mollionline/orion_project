import json

from django.http import JsonResponse, Http404

# Create your views here.
from rest_framework import generics, filters
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from api_v1.views import UserPermission
from .serializers import UserSerializers
from .models import User
from rest_framework.response import Response


class CreateUserAPIView(GenericAPIView):
    """Создать клиента"""
    permission_classes = [UserPermission]
    serializer_class = UserSerializers

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        serializer = UserSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            response = JsonResponse({'errors': serializer.errors})
            response.status_code = 400
            return response


class DeleteUserAPIView(GenericAPIView):
    """Удалить клиента"""
    permission_classes = [UserPermission]
    serializer_class = UserSerializers

    def get_queryset(self):
        return User.objects.all()

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return JsonResponse({'deleted user pk': user.pk})


class UpdateUserAPIView(generics.GenericAPIView):
    """Обновить инф о клиенте и дать право клиента при необходимости"""
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().exclude(is_staff=True)
    serializer_class = UserSerializers
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь обновлен"})
        else:
            return Response({"message": "Ошибка", "details": serializer.errors})


class UserListAPIView(generics.ListAPIView):
    """Список клиентов и фильтрация по юзернейму и по email"""
    serializer_class = UserSerializers
    queryset = User.objects.all().exclude(is_staff=True)
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

