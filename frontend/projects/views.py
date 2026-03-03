from django.shortcuts import render,get_object_or_404
from .models import Project, Task, Progress, AIInsight
from .planner import generate_tasks
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta
from .critic import run_critic
from .monitor import check_project_overdue
from django.contrib.auth.decorators import login_required
from .orchestrator import run_post_task_agents
from .diagram_generator import generate_usecase_diagram
from django.http import FileResponse

from .plantuml_generator import generate_usecase_diagram


@login_required
def dashboard(request):
    projects=Project.objects.all()
    return render(request,'projects/dashboard.html',{'projects':projects})


def project_detail(request, project_id):
    project=get_object_or_404(Project,id=project_id)
    check_project_overdue(project)
    return render(request,'projects/project_detail.html',{'project':project})

@login_required
def create_project(request):
    if request.method=="POST":
        goal=request.POST.get("goal")
        total_days=int(request.POST.get("total_days"))

        #create project first
        project=Project.objects.create(
            user=request.user,
            goal=goal,
            total_days=total_days

        )
        try:
            tasks=generate_tasks(goal,total_days)
            current_date=project.start_date
            for t in tasks:
                estimated=int(t.get("estimated_days",1))
                due_date=current_date+timedelta(days=estimated)
                Task.objects.create(
                    project=project,
                    title=t.get('title',"Untitled Task"),
                    description=t.get("description",""),
                    priority=t.get("priority","medium"),
                    estimated_days=t.get("estimated_days",1),
                    due_date=due_date
                )
                current_date=due_date
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

            #setting an timeline for the future pending tasks
            future_tasks=Task.objects.filter(
                project=task.project,
                status="pending",
                due_date__gt=task.due_date  
            ).order_by("due_date")

            for ft in future_tasks:
                ft.due_date=ft.due_date+timedelta(days=delay)
                ft.save()

            AIInsight.objects.create(
                project=task.project,
                agent_type="scheduler",
                message=f"Task {task.title} was delayed by {delay} days."
                f"{future_tasks.count()} future_tasks were rescheduled."
            )
        # run_critic(task.project)
        # check_project_overdue(task.project)
        run_post_task_agents(task.project)
        
        

        return redirect("project_detail",project_id=task.project.id)
    return render(request,"projects/complete_task.html",{"task":task})


from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(request, "auth/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "auth/login.html", {"error": "Invalid credentials"})

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# @login_required
# def generate_usecase_view(request, project_id):
#     project = get_object_or_404(Project, id=project_id)

#     diagram_code = generate_usecase_diagram(project)

#     return render(request, "projects/usecase_diagram.html", {
#         "diagram_code": diagram_code,
#         "project": project
#     })

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Project




@login_required
def usecase_diagram_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    diagram_data = generate_usecase_diagram(project)

    return render(request, "projects/usecase_diagram.html", {
        "image_url": diagram_data["image_url"],
        "project": project
    })


@login_required
def download_usecase_diagram(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    diagram_data = generate_usecase_diagram(project)

    file_path = diagram_data["image_path"]

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=f"usecase_project_{project.id}.png"
    )
