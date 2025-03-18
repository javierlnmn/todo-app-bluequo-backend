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

    def perform_update(self, serializer):
        todo = self.get_object()
        if self.request.user == todo.user or self.request.user.is_staff:
            serializer.save()
        else:
            return Response({"error": "You are not allowed to modify this todo"}, status=403)

    @action(detail=True, methods=['POST'])
    def assign(self, request, pk=None):
        todo = self.get_object()
        user_id = request.data.get('user_id')

        try:

            user = CustomUser.objects.get(id=user_id)
            todo.assigned_to = user
            todo.save()

            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=400)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.get_object().user)
