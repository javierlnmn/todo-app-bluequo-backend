from django.urls import reverse_lazy

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser


class JWTAuthTestCase(APITestCase):

    def get_jwt_token(self, username, password):
        response = self.client.post('/api/v1/users/login/', {'username': username, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

class AuthTestCase(APITestCase):

    def setUp(self):
        self.signup_url = reverse_lazy('users:signup')
        self.login_url = reverse_lazy('users:login')
        self.test_token_url = reverse_lazy('users:test-token')
        
        self.user_data = {
            'username': 'user',
            'password': 'userpassword'
        }
        self.user = CustomUser.objects.create(username=self.user_data['username'])
        self.user.set_password(self.user_data['password'])
        self.user.save()

    def test_signup(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_test_token_valid(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.test_token_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_test_token_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        response = self.client.get(self.test_token_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
