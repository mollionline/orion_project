from rest_framework import serializers
from api_v1.models import Apartment, Node, Device, Meter


class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['uuid', 'geo', 'name', 'description', 'owner', 'address', 'node_permission']
        read_only_fields = ['uuid']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['uuid', 'dev_eui', 'updated_at', 'activated_at',
                  'on_off', 'description', 'type', 'owner', 'device_permission', 'apartment', 'house']
        read_only_fields = ['uuid']


class DeviceSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['uuid', 'dev_eui', 'updated_at', 'activated_at',
                  'on_off', 'description', 'type', 'owner', 'device_permission', 'apartment', 'house']
        read_only_fields = ['uuid', 'apartment', 'house']


class MeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meter
        fields = ['uuid', 'serial_number', 'on_off', 'registration',
                  'first_testify_date', 'start_value', 'measure', 'meter_permission']
        read_only_fields = ['uuid']
