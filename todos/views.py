from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth.models import User

from users.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

from .models import Todo, Comment
from .serializers import TodoSerializer, CommentSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by('-created_at')
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, assigned_to=None)

    def perform_update(self, serializer):
        todo = self.get_object()
        if self.request.user == todo.created_by or self.request.user.is_staff:
            serializer.save()
        else:
            return Response({"error": "You are not allowed to modify this todo"}, status=403)

    @action(detail=True, methods=['POST'])
    def assign(self, request, pk=None):
        todo = self.get_object()
        user_id = request.data.get('user_id')

        try:

            user = User.objects.get(id=user_id)
            todo.assigned_to = user
            todo.save()

            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=400)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.get_object().user)
