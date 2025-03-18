from datetime import timedelta

from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import CustomUser

from .models import Todo

class TodoViewSetTestCase(APITestCase):

    def setUp(self):
        self.admin = CustomUser.objects.create(username="admin", is_staff=True, is_superuser=True)
        self.admin.set_password("adminpassword")
        self.admin.save()
        
        self.user = CustomUser.objects.create(username="user")
        self.user.set_password("userpassword")
        self.user.save()
        
        self.due_date = timezone.now().date() + timedelta(days=3)
        self.todo_1 = Todo.objects.create(title="Todo 1", due_date=self.due_date, user=self.user)
        self.todo_2 = Todo.objects.create(title="Todo 2", due_date=self.due_date, user=self.admin)

    def get_jwt_token(self, username, password):
        response = self.client.post('/api/v1/users/login/', { 'username': username, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_create_todo(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.post('/api/v1/todos/todos/', { 'title': 'New Todo', 'due_date': self.due_date, })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_todo_owner(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.put(f'/api/v1/todos/todos/{self.todo_1.id}/', { 'title': 'Updated Todo', 'due_date': self.due_date, })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_todo_non_owner(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.put(f'/api/v1/todos/todos/{self.todo_2.id}/', { 'title': 'Updated Todo', 'due_date': self.due_date, })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_todo_admin(self):
        token = self.get_jwt_token('admin', 'adminpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.put(f'/api/v1/todos/todos/{self.todo_1.id}/', { 'title': 'Updated by Admin', 'due_date': self.due_date, })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_assign_todo_admin(self):
        token = self.get_jwt_token('admin', 'adminpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        user_to_assign = CustomUser.objects.create(username="user2")
        user_to_assign.set_password("user2password")
        
        response = self.client.post(f'/api/v1/todos/todos/{self.todo_1.id}/assign/', { 'user_id': user_to_assign.id })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.todo_1.refresh_from_db()
        self.assertEqual(self.todo_1.assigned_to, user_to_assign)

    def test_assign_todo_owner(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        user_to_assign = CustomUser.objects.create(username="user2")
        user_to_assign.set_password("user2password")
        
        response = self.client.post(f'/api/v1/todos/todos/{self.todo_1.id}/assign/', { 'user_id': user_to_assign.id })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.todo_1.refresh_from_db()
        self.assertEqual(self.todo_1.assigned_to, user_to_assign)

    def test_assign_todo_non_owner(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        user_to_assign = CustomUser.objects.create(username="user2")
        user_to_assign.set_password("user2password")
        
        response = self.client.post(f'/api/v1/todos/todos/{self.todo_2.id}/assign/', { 'user_id': user_to_assign.id })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
