import requests

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .serializers import UserSignUpSerializer, UserReadSerializer, UserLoginSerializer

from .models import CustomUser


class SignupView(CreateAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        read_serializer = UserReadSerializer(instance=user)

        return Response(
            { 'access': access_token, 'refresh': str(refresh), 'user': read_serializer.data },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):

    def post(self, request, *args, **kwargs):

        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        read_serializer = UserReadSerializer(instance=user)

        return Response(
            { 'access': access_token, 'refresh': str(refresh), 'user': read_serializer.data },
            status=status.HTTP_200_OK
        )


class TestTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserReadSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserReadSerializer
    permission_classes = [IsAuthenticated]
