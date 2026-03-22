from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('overdue', 'Overdue'),
    ]
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    goal=models.TextField()
    total_days=models.IntegerField()
    start_date=models.DateField(auto_now=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    completion_rate=models.FloatField(default=0)
    risk_level=models.CharField(max_length=20, default='low')
    delayed_tasks=models.IntegerField(default=0)
    


    def __str__(self):
        return self.goal
    

class Task(models.Model):
    PRIPORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    priority=models.CharField(max_length=20, choices=PRIPORITY_CHOICES, default='medium')
    estimated_days=models.IntegerField()
    due_date=models.DateField(null=True,blank=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


    def __str__(self):
        return self.title
    
class Progress(models.Model):
    task=models.ForeignKey(Task, on_delete=models.CASCADE, related_name='progress')
    actual_days=models.IntegerField()
    completed_at=models.DateField(auto_now_add=True)


    def __str__(self):
        return f"Progress for {self.task.title}"
    

class AIInsight(models.Model):
    AGENT_CHOICES = [
        ('planner', 'Planner Agent'),
        ('analyzer', 'Analyzer Agent'),
        ('optimizer', 'Optimizer Agent'),
    ]

    project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='insights')
    agent_type=models.CharField(max_length=20, choices=AGENT_CHOICES)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Insight from {self.agent_type} for {self.project.goal}"
    

class ProjectMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=[("user", "User"), ("assistant", "Assistant"), ("system", "System")])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.role} msg on {self.project.goal[:20]}"
