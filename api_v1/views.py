import json

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

from .serializers import (UserSigninSerializer, UserSerializer, NodeSerializer,
                          DeviceSerializer, DeviceSerializerUpdate, MeterSerializer,
                          ApartmentSerializer)
from .authentication import token_expire_handler, expires_in
from .models import Apartment, House, Node, Device, Meter


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


class UpdateNodeAPIView(GenericAPIView):
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


class CreateDeviceAPIView(GenericAPIView):
    """Создать устройство в привязке к квартире"""
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

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
        data['apartment'] = apartment.pk
        data['house'] = None
        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            response = JsonResponse({'errors': serializer.errors})
            response.status_code = 400
            return response


class DeleteDeviceAPIView(GenericAPIView):
    """Удалить устройство"""
    permission_classes = [UserPermission]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.all()

    def get_object(self, uuid):
        try:
            return Device.objects.get(uuid=uuid)
        except Device.DoesNotExist:
            raise Http404

    def delete(self, request, uuid):
        device = self.get_object(uuid)
        device.delete()
        return JsonResponse({'deleted device uuid': device.uuid})


class UpdateDeviceAPIView(GenericAPIView):
    """Редактировать устройство по uuid"""
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializerUpdate
    lookup_field = 'uuid'

    def get_queryset(self):
        return Device.objects.all()

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DeviceSerializerUpdate(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            response = JsonResponse({'errors': serializer.errors})
            response.status_code = 400
            return response


class DevicesListAPIView(generics.ListAPIView):
    """Список устройств и фильтрация по приведенным полям"""
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['dev_eui', 'owner', 'uuid']


class CreateMeterAPIView(GenericAPIView):
    """Создать счетчик в привязке к квартире"""
    permission_classes = [IsAuthenticated]
    serializer_class = MeterSerializer

    def get_queryset(self):
        return Device.objects.all()

    def get_object(self, uuid):
        try:
            return Device.objects.get(uuid=uuid)
        except Apartment.DoesNotExist:
            raise Http404

    def post(self, request, uuid, *args, **kwargs):
        device = self.get_object(uuid)
        data = json.loads(request.body)
        serializer = MeterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            device.meter.add(serializer.data.get('uuid'))
            return JsonResponse(serializer.data, safe=False)
        else:
            response = JsonResponse({'errors': serializer.errors})
            response.status_code = 400
            return response


class DeleteMeterAPIView(GenericAPIView):
    """Удалить счетчик"""
    permission_classes = [UserPermission]
    serializer_class = MeterSerializer

    def get_queryset(self):
        return Meter.objects.all()

    def get_object(self, uuid):
        try:
            return Meter.objects.get(uuid=uuid)
        except Meter.DoesNotExist:
            raise Http404

    def delete(self, request, uuid):
        meter = self.get_object(uuid)
        meter.delete()
        return JsonResponse({'deleted meter uuid': meter.uuid})


class MeterListAPIView(generics.ListAPIView):
    """Список счетчиков и фильтрация по приведенным полям"""
    serializer_class = MeterSerializer
    queryset = Meter.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['serial_number', 'uuid']


class UpdateMeterAPIView(GenericAPIView):
    """Редактировать счетчик по uuid"""
    permission_classes = [IsAuthenticated]
    serializer_class = MeterSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Meter.objects.all()

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MeterSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            response = JsonResponse({'errors': serializer.errors})
            response.status_code = 400
            return response


class ApartmentFilterMeterAPIView(generics.ListAPIView):
    """Список счетчиков у квартир по uuid узла"""

    filter_backends = [filters.SearchFilter]
    serializer_class = ApartmentSerializer

    def get(self, request):
        filter_url = self.request.query_params.get('search', None)
        apartment = Apartment.objects.all()
        meters = ''
        if filter_url is not None:
            apartment = Apartment.objects.filter(node__uuid=filter_url).values_list('id', flat=True)
            apartment_id = int(list(apartment)[0])
            meters = Meter.objects.filter(device_meters__apartment=apartment_id).values()

        return Response(meters)


class DeviceFilterRangeDatesAPIView(generics.ListAPIView):
    """Возможность видеть показания за период"""
    filter_backends = [filters.SearchFilter]
    serializer_class = DeviceSerializer

    def get(self, request):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        devices = ''
        if start_date is not None and end_date is not None:
            devices = Device.objects.filter(updated_at__range=[start_date, end_date]).values_list('id', flat=True)
            devices_list = list(devices)

        return Response(devices)
