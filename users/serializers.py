from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import CustomUser


class UserSignInSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser 
        fields = ['id', 'username', 'password',]


class UserReadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'profile_picture',]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        try:
            user = authenticate(username=username, password=password)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Invalid username or password")
        
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        
        data["user"] = user
        return data