from rest_framework import serializers

from tasks.models import Task

from accounts.api.serializers import UserPublicSerializer

class TaskSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    class Meta:
        model = Task
        fields = [
            'user',
            'task',
            'is_completed',
            'timestamp',
            'id'
        ]
        read_only_fields = ['user']

    def vaidate(self, data):
        task = data.get('task', None)
        if task == '':
            task = None
        if task is None:
            raise serializers.ValidationError('Task cannot be empty.')
        return data


class TaskInlineSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'task',
            'is_completed',
            'timestamp'
        ]
