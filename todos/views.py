from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import CustomUser

from .permissions import IsAdminOwnerOrReadOnly

from .models import Todo, Comment
from .serializers import TodoSerializer, CommentSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by('-created_at')
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated, IsAdminOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
