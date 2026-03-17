import os
import subprocess
import time
from django.conf import settings

PLANTUML_JAVA_PATH = "java"
PLANTUML_JAR_PATH = "/app/plantuml.jar"


def generate_dfd_level1(project):

    plantuml_code = f"""
@startuml

rectangle "User" as User

circle "Planner Agent" as P1
circle "Scheduler Agent" as P2
circle "Critic Agent" as P3
circle "Monitor Agent" as P4
circle "Diagram Generator" as P5

database "Project Database" as DB

User --> P1 : Project Goal

P1 --> P2 : Generated Tasks

P2 --> DB : Store Scheduled Tasks
DB --> P3 : Retrieve Task Data

P3 --> P4 : Project Health Analysis

P4 --> P5 : Insights & Alerts

P5 --> User : Generated Diagrams

@enduml
"""

    diagrams_path = os.path.join(settings.MEDIA_ROOT, "diagrams")
    os.makedirs(diagrams_path, exist_ok=True)

    filename = f"dfd_level1_project_{project.id}_{int(time.time())}.puml"
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