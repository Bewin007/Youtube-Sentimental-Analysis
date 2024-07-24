from rest_framework import serializers
from rest_framework import exceptions
from .models import scraped_data,User,prof,Files
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class scraped_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = scraped_data
        fields = '__all__'

class prof_Serializer(serializers.ModelSerializer):
    class Meta:
        model = prof
        fields = '__all__'

class files_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'



# Login and reg
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')