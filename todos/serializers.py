from rest_framework import serializers

from users.serializers import UserReadSerializer
from users.models import CustomUser

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
    assignedTo = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False, allow_null=True, source='assigned_to')
    dueDate = serializers.DateField(source='due_date')
    comments = CommentSerializer(many=True, read_only=True)
    status = serializers.ChoiceField(choices=Todo.STATUS_CHOICES, required=False, allow_null=True)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['id'] = str(repr['id'])
        if instance.assigned_to:
            assigned_to_data = UserReadSerializer(instance.assigned_to).data
            repr['assignedTo'] = assigned_to_data
        else:
            repr['assignedTo'] = None
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
