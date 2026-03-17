from datetime import date
from .models import Task,AIInsight

def check_project_overdue(project):
    if project.status=='completed':
        return 
    
    last_task=Task.objects.filter(project=project).order_by('-due_date').first()

    if not last_task:
        return
    
    if date.today() > last_task.due_date:
        project.status='overdue'
        project.risk_level='high'
        project.save()

        AIInsight.objects.create(
            project=project,
            agent_type='monitor',
            message="Project has exceeded its due date and is now overdue. Risk level set to high."
        )