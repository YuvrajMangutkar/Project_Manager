from django.shortcuts import render,get_object_or_404
from .models import Project, Task, Progress, AIInsight
from .planner import generate_tasks
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta
import logging

logger = logging.getLogger(__name__)
from .critic import run_critic
from .monitor import check_project_overdue
from django.contrib.auth.decorators import login_required
from .orchestrator import run_post_task_agents
from .diagram_generator import generate_usecase_diagram
from django.http import FileResponse
from .forms import TaskForm

from .plantuml_generator import generate_usecase_diagram


@login_required
def dashboard(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects/dashboard.html', {'projects': projects})


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
            import traceback
            error_detail = traceback.format_exc()
            logger.error(f"Planner error for project {project.id}: {e}\n{error_detail}")
            # Save the error as a visible AI insight on the project
            AIInsight.objects.create(
                project=project,
                agent_type="planner",
                message=f"⚠️ Task generation failed: {e}\n\nCheck your GROQ_API_KEY in Render environment variables."
            )
        
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
                agent_type="planner",
                message=f"Task '{task.title}' was delayed by {delay} days. "
                f"{future_tasks.count()} future tasks were rescheduled."
            )
        # run_critic(task.project)
        # check_project_overdue(task.project)
        run_post_task_agents(task.project)
        
        

        return redirect("project_detail",project_id=task.project.id)
    return render(request,"projects/complete_task.html",{"task":task})


@login_required
def add_task(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = TaskForm()
    return render(request, "projects/add_task.html", {"form": form, "project": project})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("project_detail", project_id=task.project.id)
    else:
        form = TaskForm(instance=task)
    return render(request, "projects/edit_task.html", {"form": form, "task": task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__user=request.user)
    if request.method == "POST":
        project_id = task.project.id
        task.delete()
        return redirect("project_detail", project_id=project_id)
    # If accessed via GET, redirect back
    return redirect("project_detail", project_id=task.project.id)


@login_required
def gantt_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    tasks = list(Task.objects.filter(project=project).order_by("due_date", "id"))
    
    # Calculate start offsets for each task
    gantt_tasks = []
    current_offset = 0
    
    for t in tasks:
        # If task has a specific due date, we can calculate actual dates,
        # but a simple relative offset works best for the visual chart
        duration = t.estimated_days or 1
        
        gantt_tasks.append({
            "id": t.id,
            "title": t.title,
            "priority": t.priority,
            "status": t.status,
            "duration": duration,
            "start_offset": current_offset,
            "due_date": t.due_date.strftime("%b %d, %Y") if t.due_date else "N/A"
        })
        current_offset += duration

    return render(request, "projects/gantt.html", {
        "project": project,
        "gantt_tasks": gantt_tasks,
        "total_duration": current_offset if current_offset > 0 else 1
    })


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
        "plantuml_code": diagram_data.get("plantuml_code", ""),
        "project": project
    })


# download_usecase_diagram removed — diagrams are served directly from PlantUML server URL.
# Use the image_url from the view context to download via the browser.

from .dfd_level0_generator import generate_dfd_level0


@login_required
def dfd_level0_view(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    diagram = generate_dfd_level0(project)

    return render(request, "projects/dfd_level0.html", {
        "image_url": diagram["image_url"],
        "plantuml_code": diagram.get("plantuml_code", ""),
        "project": project
    })


# download_dfd_level0 removed — diagrams are served directly from PlantUML server URL.

from .dfd_level1_generator import generate_dfd_level1
from django.http import FileResponse


@login_required
def dfd_level1_view(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    diagram = generate_dfd_level1(project)

    return render(request, "projects/dfd_level1.html", {
        "image_url": diagram["image_url"],
        "plantuml_code": diagram.get("plantuml_code", ""),
        "project": project
    })


# download_dfd_level1 removed — diagrams are served directly from PlantUML server URL.

from .activity_generator import generate_activity_diagram



@login_required
def activity_diagram_view(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    diagram = generate_activity_diagram(project)

    return render(request, "projects/activity_diagram.html", {
        "image_url": diagram["image_url"],
        "plantuml_code": diagram.get("plantuml_code", ""),
        "project": project
    })


# download_activity_diagram removed — diagrams are served directly from PlantUML server URL.


# ── Diagram Proxy Download View ───────────────────────────────────────────────
# The 'download' attribute on <a> tags doesn't work for cross-origin URLs.
# This view fetches the PlantUML image server-side and streams it as a download.
@login_required
def download_diagram(request):
    import requests as req_lib
    from django.http import HttpResponse

    image_url = request.GET.get("url", "")
    filename = request.GET.get("name", "diagram.png")

    if not image_url or "plantuml.com" not in image_url:
        return HttpResponse("Invalid or missing diagram URL.", status=400)

    try:
        resp = req_lib.get(image_url, timeout=15)
        resp.raise_for_status()
        response = HttpResponse(resp.content, content_type="image/png")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        return HttpResponse(f"Failed to fetch diagram: {e}", status=502)




# ── Groq Diagnostic View ─────────────────────────────────────────────────────
# Visit /debug/groq/ in production to see exactly why task generation fails.
# Remove this view once everything works.
import os
from django.http import HttpResponse

@login_required
def groq_debug_view(request):
    import traceback
    lines = []

    api_key = os.getenv("GROQ_API_KEY", "")
    lines.append(f"GROQ_API_KEY set: {'YES — ' + api_key[:10] + '...' if api_key else 'NO (empty)'}")
    lines.append(f"GROQ_MODEL: {os.getenv('GROQ_MODEL', 'llama3-8b-8192 (default)')}")
    lines.append("")

    if not api_key:
        lines.append("❌ GROQ_API_KEY is missing. Set it in Render → Environment.")
        return HttpResponse("\n".join(lines), content_type="text/plain")

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama3-8b-8192"),
            messages=[{"role": "user", "content": "Reply with the single word: WORKING"}],
            temperature=0,
        )
        raw = response.choices[0].message.content
        lines.append(f"✅ Groq connection OK. Raw response: {raw!r}")
    except Exception as e:
        lines.append(f"❌ Groq call FAILED: {e}")
        lines.append("")
        lines.append(traceback.format_exc())

    lines.append("")
    lines.append("--- Full task generation test ---")
    try:
        from .planner import _generate_with_groq
        tasks = _generate_with_groq("Build a simple todo app", 7)
        lines.append(f"✅ Task generation OK — {len(tasks)} tasks returned")
        for t in tasks:
            lines.append(f"  • {t.get('title', '?')} ({t.get('priority','?')}, {t.get('estimated_days','?')} days)")
    except Exception as e:
        lines.append(f"❌ Task generation FAILED: {e}")
        lines.append(traceback.format_exc())

    return HttpResponse("\n".join(lines), content_type="text/plain")