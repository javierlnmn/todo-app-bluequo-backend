from django.db import models

from users.models import CustomUser


class Todo(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In progress'),
        ('COMPLETED', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='PENDING')
    due_date = models.DateField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_todos')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_todos')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.description}'

class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s comment in todo {self.todo.title}'
