from .plantuml_encoder import plantuml_url
from .models import Task


def generate_activity_diagram(project):
    """
    Activity Diagram via PlantUML public server.
    - Dark theme skinparams
    - Decision nodes for task status (completed/overdue/pending)
    - Priority-based colors (high=red, medium=orange, low=green)
    - Branching for delayed task rescheduling
    """
    tasks = Task.objects.filter(project=project).order_by("id")

    def safe(title):
        return title.replace("(", "").replace(")", "").replace('"', "").strip()

    code = "@startuml\n"
    code += "skinparam backgroundColor #1E293B\n"
    code += "skinparam defaultFontColor #F1F5F9\n"
    code += "skinparam defaultFontName Arial\n"
    code += "skinparam defaultFontSize 13\n"
    code += "skinparam ArrowColor #6366F1\n"
    code += "skinparam ArrowThickness 2\n"
    code += "skinparam ActivityBorderColor #334155\n"
    code += "skinparam ActivityBackgroundColor #0F172A\n"
    code += "skinparam ActivityFontColor #F1F5F9\n"
    code += "skinparam ActivityDiamondBackgroundColor #1E293B\n"
    code += "skinparam ActivityDiamondBorderColor #6366F1\n"
    code += "skinparam ActivityDiamondFontColor #F1F5F9\n"
    code += "skinparam NoteBackgroundColor #1E293B\n"
    code += "skinparam NoteBorderColor #475569\n"
    code += "skinparam NoteFontColor #94A3B8\n"
    code += "skinparam StartColor #6366F1\n"
    code += "skinparam EndColor #EF4444\n"

    code += "\nstart\n\n"
    code += "#6366F1:📋 Create Project Goal;\n"
    code += "#10B981:🤖 AI Generates Task Plan;\n\n"

    code += "if (Tasks Generated?) then (yes)\n"
    code += "else (no)\n"
    code += "  #EF4444:⚠️ Show Fallback Task;\n"
    code += "  stop\n"
    code += "endif\n\n"

    for task in tasks:
        title = safe(task.title)
        # Color the activity based on priority
        if task.priority == "high":
            color = "#7F1D1D"    # dark red
            prefix = "🔴"
        elif task.priority == "medium":
            color = "#78350F"    # dark amber
            prefix = "🟡"
        else:
            color = "#14532D"    # dark green
            prefix = "🟢"

        code += f"{color}:{prefix} {title};\n"
        code += "note right\n"
        code += f"  Priority: {task.priority.capitalize()}\n"
        code += f"  Est. Days: {task.estimated_days}\n"
        if task.due_date:
            code += f"  Due: {task.due_date}\n"
        code += "end note\n\n"

        # Decision node per task
        code += f"if ({title} Status?) then (completed)\n"

        # Check if it took longer than estimated
        progress_qs = task.progress.all()
        if progress_qs.exists():
            actual = progress_qs.first().actual_days
            if actual > task.estimated_days:
                delay = actual - task.estimated_days
                code += f"  #7C3AED:⚠️ Delayed by {delay} day(s);\n"
                code += "  #4C1D95:🔄 Reschedule Future Tasks;\n"
            else:
                code += "  #065F46:✅ On Time;\n"
        else:
            code += "  #065F46:✅ On Time;\n"

        code += "elseif (overdue) then\n"
        code += f"  #7F1D1D:🚨 Overdue — Alert Monitor Agent;\n"
        code += "else (pending)\n"
        code += f"  #1E3A5F:⏳ In Queue;\n"
        code += "endif\n\n"

    code += "#0F172A:📊 Analyze Project Health;\n"
    code += "if (Risk Level?) then (high)\n"
    code += "  #7F1D1D:🚨 Raise Risk Alert;\n"
    code += "elseif (medium) then\n"
    code += "  #78350F:⚠️ Log Warning Insight;\n"
    code += "else (low)\n"
    code += "  #14532D:✅ Project On Track;\n"
    code += "endif\n\n"
    code += "#1E293B:📐 Generate Diagrams;\n"
    code += "\nstop\n"
    code += "@enduml"

    url = plantuml_url(code)
    return {
        "image_url": url,
        "image_path": None,
        "plantuml_code": code,
    }