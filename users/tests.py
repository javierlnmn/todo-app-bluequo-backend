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


class UserViewSetTestCase(JWTAuthTestCase):

    def setUp(self):
        self.user_data = {
            'username': 'user1',
            'password': 'userpassword'
        }
        self.user = CustomUser.objects.create(username=self.user_data['username'])
        self.user.set_password(self.user_data['password'])
        self.user.save()

        self.admin_data = {
            'username': 'admin',
            'password': 'adminpassword'
        }
        self.admin = CustomUser.objects.create(username=self.admin_data['username'], is_staff=True)
        self.admin.set_password(self.admin_data['password'])
        self.admin.save()

        self.users_url = reverse_lazy('users:user-list')

    def test_list_users_authenticated(self):
        """Test that an authenticated user can list users"""
        token = self.get_jwt_token(self.user_data['username'], self.user_data['password'])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data[0])  # Check if the response contains 'username'
        self.assertEqual(response.data[0]['username'], self.user_data['username'])

    def test_list_users_unauthenticated(self):
        """Test that unauthenticated users are not allowed to list users"""
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user(self):
        token = self.get_jwt_token(self.user_data['username'], self.user_data['password'])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        user_detail_url = reverse_lazy('users:user-detail', kwargs={'pk': self.user.id})  
        response = self.client.get(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_retrieve_user_without_token(self):
        """Test that retrieving user data without token should be unauthorized"""
        user_detail_url = reverse_lazy('users:user-detail', kwargs={'pk': self.user.id})
        response = self.client.get(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
