from rest_framework import serializers

from users.serializers import UserReadSerializer

from .models import Todo, Comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'todo',
            'user',
            'content',
        )
        read_only_fields = (
            'id',
            'created_at'
        )


class TodoSerializer(serializers.ModelSerializer):
    assigned_to = UserReadSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Todo
        fields = (
            'id',
            'title',
            'description',
            'status',
            'due_date',
            'assigned_to',
            'comments'
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at'
        )
