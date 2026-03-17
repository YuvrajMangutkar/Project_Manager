import os
import subprocess
import time
from django.conf import settings
from .models import Task


# 🔹 Update these paths if needed
PLANTUML_JAVA_PATH = "java"
PLANTUML_JAR_PATH = "/app/plantuml.jar"


def generate_usecase_diagram(project):
    """
    Generates a dynamic UML Use Case Diagram for a specific project.
    """

    # Fetch tasks for this project
    tasks = Task.objects.filter(project=project)

    # Start building PlantUML code
    plantuml_code = "@startuml\n"
    plantuml_code += "actor User\n"
    plantuml_code += f'rectangle "{project.goal}" {{\n\n'

    # 🔹 Core system capabilities
    plantuml_code += "  User --> (Create Project)\n"
    plantuml_code += "  User --> (Track Tasks)\n"
    plantuml_code += "  User --> (View Project Health)\n"
    plantuml_code += "  User --> (Generate Diagrams)\n\n"

    plantuml_code += "  (Track Tasks) --> (Complete Task)\n"
    plantuml_code += "  (Track Tasks) --> (Update Progress)\n\n"

    # 🔹 Dynamically include project-specific tasks
    for task in tasks:
        # Clean unsafe characters
        safe_title = (
            task.title
            .replace("(", "")
            .replace(")", "")
            .replace('"', "")
            .strip()
        )

        plantuml_code += f'  (Track Tasks) ..> ({safe_title}) : <<include>>\n'

    plantuml_code += "\n}\n@enduml"

    # 🔹 Create diagrams directory
    diagrams_path = os.path.join(settings.MEDIA_ROOT, "diagrams")
    os.makedirs(diagrams_path, exist_ok=True)

    # 🔹 Unique filename to avoid browser caching
    filename = f"usecase_project_{project.id}_{int(time.time())}.puml"
    file_path = os.path.join(diagrams_path, filename)

    # Save .puml file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(plantuml_code)

    # Generate PNG using PlantUML engine
    subprocess.run([
        PLANTUML_JAVA_PATH,
        "-jar",
        PLANTUML_JAR_PATH,
        file_path
    ])

    # Return image URL
    image_name = filename.replace(".puml", ".png")
    return {
    "image_url": f"/media/diagrams/{image_name}",
    "image_path": os.path.join(diagrams_path, image_name)
}