from .plantuml_encoder import plantuml_url


def generate_dfd_level1(project):
    """DFD Level 1 (Internal Agents) via PlantUML public server."""
    code = """@startuml
skinparam backgroundColor #FAFAFA

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

@enduml"""

    url = plantuml_url(code)
    return {
        "image_url": url,
        "image_path": None,
        "plantuml_code": code,
    }