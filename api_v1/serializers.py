from rest_framework import serializers
from api_v1.models import Apartment, Node


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