from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

@api_view(['POST'])
def check_overdue_tasks(request):
    """
    Check and mark tasks as OVERDUE if:
    1. due_date is in the past
    2. status is not DONE
    """
    try:
        today = timezone.now().date()
        
        # Find all tasks past due date that are not DONE
        overdue_tasks = Task.objects.filter(
            due_date__lt=today,
            status__in=['TODO', 'IN_PROGRESS']
        )
        
        # Mark them as OVERDUE
        count = 0
        for task in overdue_tasks:
            if task.mark_overdue_if_applicable():
                count += 1
        
        return Response({
            'message': f'{count} tasks marked as OVERDUE',
            'count': count,
            'timestamp': timezone.now()
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def validate_task_transition(request):
    """
    Validate if a task can transition to a new status
    Rules:
    1. OVERDUE tasks cannot move back to IN_PROGRESS
    2. Only admin can close (mark as DONE) OVERDUE tasks
    """
    try:
        task_id = request.data.get('task_id')
        new_status = request.data.get('status')
        is_admin = request.data.get('is_admin', False)
        
        if not task_id or not new_status:
            return Response({
                'error': 'task_id and status are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        task = Task.objects.get(id=task_id)
        
        # Rule 1: OVERDUE tasks cannot move back to IN_PROGRESS
        if task.status == 'OVERDUE' and new_status == 'IN_PROGRESS':
            return Response({
                'allowed': False,
                'reason': 'Overdue tasks cannot move back to IN_PROGRESS'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Rule 2: Only admin can close OVERDUE tasks
        if task.status == 'OVERDUE' and new_status == 'DONE' and not is_admin:
            return Response({
                'allowed': False,
                'reason': 'Only admins can close overdue tasks'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # All checks passed
        return Response({
            'allowed': True,
            'task_id': task_id,
            'current_status': task.status,
            'new_status': new_status
        }, status=status.HTTP_200_OK)
    
    except Task.DoesNotExist:
        return Response({
            'error': f'Task {task_id} not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_overdue_tasks(request):
    """Get all overdue tasks"""
    try:
        overdue_tasks = Task.objects.filter(status='OVERDUE')
        serializer = TaskSerializer(overdue_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

