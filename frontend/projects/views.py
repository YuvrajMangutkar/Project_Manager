from django.shortcuts import render,get_object_or_404
from .models import Project, Task, Progress, AIInsight
from .planner import generate_tasks
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .critic import run_critic


def dashboard(request):
    projects=Project.objects.all()
    return render(request,'projects/dashboard.html',{'projects':projects})


def project_detail(request, project_id):
    project=get_object_or_404(Project,id=project_id)
    return render(request,'projects/project_detail.html',{'project':project})

@login_required
def create_project(request):
    if request.method=="POST":
        goal=request.POST.get("goal")
        total_days=request.POST.get("total_days")

        #create project first
        project=Project.objects.create(
            user=request.user,
            goal=goal,
            total_days=int(total_days)

        )
        try:
            tasks=generate_tasks(goal,total_days)

            for t in tasks:
                Task.objects.create(
                    project=project,
                    title=t.get('title',"Untitled Task"),
                    description=t.get("description",""),
                    priority=t.get("priority","medium"),
                    estimated_days=t.get("estimated_days",1)
                )
        except Exception as e:
            print("Planner error:",e)
        
        return redirect("dashboard")
    return render(request,"projects/create_project.html")

def complete_task(request,task_id):
    task=Task.objects.get(id=task_id)
    if request.method=="POST":
        actual_days=int(request.POST.get("actual_days"))
        task.status="completed"
        task.save()
        Progress.objects.create(
            task=task,
            actual_days=actual_days

        )

        if actual_days>task.estimated_days:
            delay=actual_days-task.estimated_days

            AIInsight.objects.create(
                project=task.project,
                agent_type="scheduler",
                message=f"Task {task.title} was delayed by {delay} days.Consider adjusting future task timelines."
            )
        run_critic(task.project)
        

        return redirect("project_detail",project_id=task.project.id)
    return render(request,"projects/complete_task.html",{"task":task})







# Create your views here.
