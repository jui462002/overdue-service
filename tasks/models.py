from django.db import models
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
        ('OVERDUE', 'Overdue'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    id = models.IntegerField(primary_key=True)  # Synced from Laravel
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    due_date = models.DateField()
    project_id = models.IntegerField()
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tasks'  # Link to Laravel's tasks table
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def is_overdue(self):
        """Check if task is past due and not completed"""
        today = timezone.now().date()
        return self.due_date < today and self.status != 'DONE'
    
    def mark_overdue_if_applicable(self):
        """Mark task as OVERDUE if conditions are met"""
        if self.is_overdue() and self.status != 'OVERDUE':
            self.status = 'OVERDUE'
            self.save()
            return True
        return False

