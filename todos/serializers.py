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
    user = UserReadSerializer(read_only=True)
    assignedTo = UserReadSerializer(read_only=True, source='assigned_to')
    dueDate = serializers.DateField(source='due_date')
    comments = CommentSerializer(many=True, read_only=True)
    status = serializers.ChoiceField(choices=Todo.STATUS_CHOICES, required=False)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['id'] = str(repr['id'])
        repr['status'] = instance.get_status_display()
        return repr

    class Meta:
        model = Todo
        fields = (
            'id',
            'title',
            'description',
            'status',
            'dueDate',
            'assignedTo',
            'comments',
            'user',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at'
        )
