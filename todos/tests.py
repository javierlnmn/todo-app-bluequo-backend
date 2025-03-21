from datetime import timedelta

from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import CustomUser
from users.tests import JWTAuthTestCase

from .models import Todo, Comment

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


class CommentViewSetTestCase(JWTAuthTestCase):
    
    def setUp(self):
        self.admin = CustomUser.objects.create(username="admin", is_staff=True, is_superuser=True)
        self.admin.set_password("adminpassword")
        self.admin.save()
        
        self.user = CustomUser.objects.create(username="user")
        self.user.set_password("userpassword")
        self.user.save()
        
        self.todo = Todo.objects.create(title="Test Todo", due_date=timezone.now().date(), user=self.user)
        self.user_comment = Comment.objects.create(todo=self.todo, user=self.user, content="Test comment")

        self.user2 = CustomUser.objects.create(username="user2")
        self.user2.set_password("user2password")
        self.user2.save()

    def test_create_comment(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.post(f'/api/v1/todos/comments/', {
            'todo': self.todo.id,
            'content': 'New comment'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_comment_owner(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.patch(f'/api/v1/todos/comments/{self.user_comment.id}/', {
            'content': 'Updated comment'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment_non_owner(self):
        token = self.get_jwt_token('user2', 'user2password')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.patch(f'/api/v1/todos/comments/{self.user_comment.id}/', {
            'content': 'User 2 updating user comment'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_comment_non_owner_admin(self):
        token = self.get_jwt_token('admin', 'adminpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.patch(f'/api/v1/todos/comments/{self.user_comment.id}/', {
            'content': 'Admin updating user comment'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment_owner(self):
        token = self.get_jwt_token('user', 'userpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.delete(f'/api/v1/todos/comments/{self.user_comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_non_owner(self):
        token = self.get_jwt_token('user2', 'user2password')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.delete(f'/api/v1/todos/comments/{self.user_comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_non_owner_admin(self):
        token = self.get_jwt_token('admin', 'adminpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.delete(f'/api/v1/todos/comments/{self.user_comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
