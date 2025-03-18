from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import CustomUser


class UserSignInSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser 
        fields = ['id', 'email', 'password',]


class UserReadSerializer(serializers.ModelSerializer):
    profile_picture = serializers.CharField(source='external_profile_picture_url')
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'profile_picture',]


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = authenticate(email=email, password=password)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Invalid email or password")
        
        if user is None:
            raise serializers.ValidationError("Invalid email or password")
        
        data["user"] = user
        return data