from .models import Task,AIInsight

def run_critic(project):
    tasks=Task.objects.filter(project=project)
    total_tasks=tasks.count()

    if total_tasks==0:
        return 
    
    completed_tasks=tasks.filter(status="completed").count()
    completion_rate=(completed_tasks)/total_tasks*100
    delayed_tasks = 0

    for task in tasks:
        progress_obj = task.progress.first()

    if progress_obj:
        if progress_obj.actual_days > task.estimated_days:
            delayed_tasks += 1
    
    if completion_rate>=80:
        risk="low"
    elif completion_rate>=50:
        risk="medium"
    else:
        risk="high"

    message = (
        f"Project Health Report\n"
        f"----------------------\n"
        f"Completion Rate: {completion_rate:.2f}%\n"
        f"Delayed Tasks: {delayed_tasks}\n"
        f"Risk Level: {risk}"
    )
    AIInsight.objects.create(
        project=project,
        agent_type="critic",
        message=message
    )
    