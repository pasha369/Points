from django.contrib.auth.models import User
from models import BaseUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'user', 'first_name',
                  'last_name')
        read_only_fields = ('id',)
        write_only_fields = ('password',)


    def create(self, validated_data):
        return BaseUser.objects.create(**validated_data)