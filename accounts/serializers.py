from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'description']
        read_only_fields = ['id']
