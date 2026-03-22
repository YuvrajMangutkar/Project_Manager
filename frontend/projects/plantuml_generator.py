from .plantuml_encoder import plantuml_url
from .models import Task


def generate_usecase_diagram(project):
    """
    Generate a themed Use Case diagram using the free PlantUML public server.
    - Tasks grouped by priority (high/medium/low)
    - AI Agent actor added
    - Proper dark-friendly skinparam theme
    """
    tasks = Task.objects.filter(project=project)

    high_tasks   = [t for t in tasks if t.priority == "high"]
    medium_tasks = [t for t in tasks if t.priority == "medium"]
    low_tasks    = [t for t in tasks if t.priority == "low"]

    def safe(title):
        return title.replace("(", "").replace(")", "").replace('"', "").strip()

    code = "@startuml\n"
    code += "skinparam backgroundColor #1E293B\n"
    code += "skinparam defaultFontColor #F1F5F9\n"
    code += "skinparam defaultFontName Arial\n"
    code += "skinparam defaultFontSize 13\n"
    code += "skinparam ArrowColor #6366F1\n"
    code += "skinparam ArrowThickness 2\n"
    code += "skinparam ActorBorderColor #6366F1\n"
    code += "skinparam ActorBackgroundColor #0F172A\n"
    code += "skinparam ActorFontColor #F1F5F9\n"
    code += "skinparam UsecaseBorderColor #6366F1\n"
    code += "skinparam UsecaseBackgroundColor #0F172A\n"
    code += "skinparam UsecaseFontColor #F1F5F9\n"
    code += "skinparam RectangleBorderColor #334155\n"
    code += "skinparam RectangleBackgroundColor #0F172A\n"
    code += "skinparam RectangleFontColor #94A3B8\n"
    code += "skinparam NoteBackgroundColor #1E293B\n"
    code += "skinparam NoteBorderColor #475569\n"
    code += "skinparam NoteFontColor #94A3B8\n"

    code += "\nactor User #6366F1\n"
    code += "actor \"AI Agent\" as AI #10B981\n\n"

    code += f'rectangle "📋 {safe(project.goal)}" {{\n\n'

    # Core user interactions
    code += "  User --> (Create Project)\n"
    code += "  User --> (View Dashboard)\n"
    code += "  User --> (Complete Task)\n"
    code += "  User --> (Generate Diagrams)\n\n"

    # AI Agent interactions
    code += "  AI --> (Generate Task Plan)\n"
    code += "  AI --> (Analyze Project Health)\n"
    code += "  AI --> (Detect Delays)\n"
    code += "  AI --> (Reschedule Future Tasks)\n\n"

    code += "  (Create Project) ..> (Generate Task Plan) : <<trigger>>\n"
    code += "  (Complete Task) ..> (Analyze Project Health) : <<trigger>>\n"
    code += "  (Analyze Project Health) ..> (Detect Delays) : <<include>>\n"
    code += "  (Detect Delays) ..> (Reschedule Future Tasks) : <<extend>>\n\n"

    # High priority tasks
    if high_tasks:
        code += "  package \"🔴 High Priority Tasks\" {\n"
        for task in high_tasks:
            code += f'    ({safe(task.title)})\n'
        code += "  }\n"
        for task in high_tasks:
            code += f'  (Generate Task Plan) ..> ({safe(task.title)}) : <<include>>\n'
        code += "\n"

    # Medium priority tasks
    if medium_tasks:
        code += "  package \"🟡 Medium Priority Tasks\" {\n"
        for task in medium_tasks:
            code += f'    ({safe(task.title)})\n'
        code += "  }\n"
        for task in medium_tasks:
            code += f'  (Generate Task Plan) ..> ({safe(task.title)}) : <<include>>\n'
        code += "\n"

    # Low priority tasks
    if low_tasks:
        code += "  package \"🟢 Low Priority Tasks\" {\n"
        for task in low_tasks:
            code += f'    ({safe(task.title)})\n'
        code += "  }\n"
        for task in low_tasks:
            code += f'  (Generate Task Plan) ..> ({safe(task.title)}) : <<include>>\n'
        code += "\n"

    code += "}\n@enduml"

    url = plantuml_url(code)
    return {
        "image_url": url,
        "image_path": None,
        "plantuml_code": code,
    }