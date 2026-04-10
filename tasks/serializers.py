from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority', 'due_date', 'project_id', 'user_id', 'created_at', 'updated_at']
