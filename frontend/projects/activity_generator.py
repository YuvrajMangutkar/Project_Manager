import os
import subprocess
import time
from django.conf import settings
from .models import Task

PLANTUML_JAVA_PATH = r"E:\java\bin\java.exe"
PLANTUML_JAR_PATH = r"D:\plantuml\plantuml.jar"


def generate_activity_diagram(project):

    tasks = Task.objects.filter(project=project).order_by("id")

    plantuml_code = "@startuml\n"
    plantuml_code += "start\n"

    plantuml_code += ":Create Project;\n"
    plantuml_code += ":Generate Task Plan;\n"

    # Dynamic task flow
    for task in tasks:
        safe_title = (
            task.title
            .replace("(", "")
            .replace(")", "")
            .replace('"', "")
            .strip()
        )

        plantuml_code += f":{safe_title};\n"

    plantuml_code += ":Analyze Project Health;\n"
    plantuml_code += ":Generate Diagrams;\n"
    plantuml_code += "stop\n"

    plantuml_code += "@enduml"

    diagrams_path = os.path.join(settings.MEDIA_ROOT, "diagrams")
    os.makedirs(diagrams_path, exist_ok=True)

    filename = f"activity_project_{project.id}_{int(time.time())}.puml"
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

    return {
        "image_url": f"/media/diagrams/{image_name}",
        "image_path": os.path.join(diagrams_path, image_name)
    }