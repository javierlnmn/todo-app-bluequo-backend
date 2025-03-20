from datetime import timedelta

from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import CustomUser
from users.tests import JWTAuthTestCase

from .models import Todo

from users.serializers import UserReadSerializer


class TodoViewSetTestCase(JWTAuthTestCase):

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

    def test_create_todo(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.post('/api/v1/todos/todos/', { 'title': 'New Todo', 'dueDate': self.due_date, })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_todo_owner(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.put(f'/api/v1/todos/todos/{self.todo_1.id}/', { 'title': 'Updated Todo', 'dueDate': self.due_date, })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_todo_non_owner(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.put(f'/api/v1/todos/todos/{self.todo_2.id}/', { 'title': 'Updated Todo', 'dueDate': self.due_date, })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_todo_admin(self):
        token = self.get_jwt_token('admin', 'adminpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.put(f'/api/v1/todos/todos/{self.todo_1.id}/', { 'title': 'Updated by Admin', 'dueDate': self.due_date, })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_todo_with_user_field(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.put(f'/api/v1/todos/todos/{self.todo_1.id}/', {
            'title': 'Updated Todo',
            'dueDate': self.due_date,
            'user': self.admin.id,
        })

        self.assertEqual(self.user.username, response.data['user']['username']) # User was not updated

    def test_update_todo_with_assignedTo_field(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.put(f'/api/v1/todos/todos/{self.todo_1.id}/', {
            'title': 'Updated Todo',
            'dueDate': self.due_date,
            'assignedTo': str(self.admin.id),
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        admin_user_serializer = UserReadSerializer(self.admin).data
        self.assertEqual(response.data['assignedTo'], admin_user_serializer)