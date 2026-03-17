import os
import subprocess
from django.conf import settings
from .models import Task

PLANTUML_JAVA_PATH = "java"
PLANTUML_JAR_PATH = "/app/plantuml.jar"


def generate_usecase_diagram(project):
    print("Project ID:", project.id)
    print("Project Goal:", project.goal)
    print("Tasks Found:", Task.objects.filter(project=project).count())
    tasks = Task.objects.filter(project=project)

    plantuml_code = "@startuml\n"
    plantuml_code += "actor User\n"
    plantuml_code += f'rectangle "{project.goal}" {{\n'

    # Main system actions
    plantuml_code += "  User --> (Create Project)\n"
    plantuml_code += "  User --> (View Dashboard)\n"

    # Add dynamic task-based use cases
    for task in tasks:
        safe_title = task.title.replace("(", "").replace(")", "")
        plantuml_code += f'  User --> ({safe_title})\n'

    plantuml_code += "}\n"
    plantuml_code += "@enduml\n"

    diagrams_path = os.path.join(settings.MEDIA_ROOT, "diagrams")
    os.makedirs(diagrams_path, exist_ok=True)

    filename = f"usecase_project_{project.id}.puml"
    file_path = os.path.join(diagrams_path, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(plantuml_code)

    subprocess.run([
        PLANTUML_JAVA_PATH,
        "-jar",
        PLANTUML_JAR_PATH,
        file_path
    ])

    image_name = filename.replace(".puml", ".png")
    return f"/media/diagrams/{image_name}"