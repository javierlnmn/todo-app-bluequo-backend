from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import CustomUser

class UserSignUpSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'confirmPassword')

    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError({"confirmPassword": "Passwords do not match"})
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create(username=validated_data['username'],)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserReadSerializer(serializers.ModelSerializer):
    isSuperuser = serializers.BooleanField(source='is_superuser')
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'isSuperuser')


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