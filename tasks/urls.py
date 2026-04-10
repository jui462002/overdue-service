from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('check-overdue/', views.check_overdue_tasks, name='check_overdue'),
    path('validate-transition/', views.validate_task_transition, name='validate_transition'),
    path('overdue-list/', views.get_overdue_tasks, name='overdue_list'),
]
