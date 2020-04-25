from rest_framework import serializers
from tasks.api.serializers import TaskInlineSerializer

from django.contrib.auth import get_user_model



User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'tasks'
        ]

    def get_tasks(self, obj):
        request = self.context.get('request')
        limit = 10
        if request:
            limit_query = request.GET.get('limit')
            try:
                limit = int(limit_query)
            except:
                pass
        qs = obj.tasks.all().order_by('-timestamp')[:limit]
        data = {
            'last': TaskInlineSerializer(qs.first()).data,
            'recent': TaskInlineSerializer(qs, many=True).data
        }
        return data
