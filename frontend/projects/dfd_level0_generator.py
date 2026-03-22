from .plantuml_encoder import plantuml_url


def generate_dfd_level0(project):
    """DFD Level 0 (Context Diagram) via PlantUML public server."""
    code = f"""@startuml
skinparam backgroundColor #FAFAFA

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

@enduml"""

    url = plantuml_url(code)
    return {
        "image_url": url,
        "image_path": None,
        "plantuml_code": code,
    }