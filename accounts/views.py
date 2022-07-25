import json

from django.http import JsonResponse, Http404

# Create your views here.
from rest_framework import generics
from rest_framework.generics import GenericAPIView
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


class UpdateUserAPIView(generics.UpdateAPIView):
    """Обновить инф о клиента"""
    permission_classes = [UserPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializers
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь обновлен"})
        else:
            return Response({"message": "Ошибка", "details": serializer.errors})


class UserListAPIView(GenericAPIView):
    """Список клиентов"""
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializers(users, many=True)
        return JsonResponse(serializer.data, safe=False)
