import os
import subprocess
import time
from django.conf import settings

PLANTUML_JAVA_PATH = r"E:\java\bin\java.exe"
PLANTUML_JAR_PATH = r"D:\plantuml\plantuml.jar"


def generate_dfd_level0(project):

    plantuml_code = f"""
@startuml

rectangle "User" as User
rectangle "AI Project Manager" as System
database "Project Database" as DB

User --> System : Project Goal
User --> System : Task Updates

System --> User : Task Plan
System --> User : Project Insights
System --> User : UML Diagrams

System --> DB : Store Project Data
DB --> System : Retrieve Tasks

@enduml
"""

    diagrams_path = os.path.join(settings.MEDIA_ROOT, "diagrams")
    os.makedirs(diagrams_path, exist_ok=True)

    filename = f"dfd_level0_project_{project.id}_{int(time.time())}.puml"
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