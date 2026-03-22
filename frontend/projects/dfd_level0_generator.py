from .plantuml_encoder import plantuml_url
from .models import Task, AIInsight


def generate_dfd_level0(project):
    """
    DFD Level 0 (Context Diagram) via PlantUML public server.
    - Dark theme skinparams
    - Uses real project data (goal, task count)
    - Groq AI shown as external entity
    """
    task_count = Task.objects.filter(project=project).count()
    completed_count = Task.objects.filter(project=project, status="completed").count()
    insight_count = AIInsight.objects.filter(project=project).count()

    code = f"""@startuml
skinparam backgroundColor #1E293B
skinparam defaultFontColor #F1F5F9
skinparam defaultFontName Arial
skinparam defaultFontSize 13
skinparam ArrowColor #6366F1
skinparam ArrowThickness 2
skinparam RectangleBorderColor #6366F1
skinparam RectangleBackgroundColor #0F172A
skinparam RectangleFontColor #F1F5F9
skinparam DatabaseBorderColor #10B981
skinparam DatabaseBackgroundColor #0F172A
skinparam DatabaseFontColor #10B981
skinparam NoteBackgroundColor #1E293B
skinparam NoteBorderColor #475569
skinparam NoteFontColor #94A3B8

rectangle "👤 User" as User #1E3A5F
rectangle "🤖 AI Project Manager\\n(Django + Groq)" as System #312E81
rectangle "⚡ Groq AI\\n(LLaMA 3)" as Groq #064E3B
database "🗄️ Project Database\\n({task_count} tasks | {completed_count} completed)" as DB #1C1917

User --> System : project goal + timeline
User --> System : task completion updates

System --> Groq : generate task plan prompt
Groq --> System : {task_count} structured tasks (JSON)

System --> User : AI-generated task plan
System --> User : {insight_count} AI insight(s)
System --> User : UML diagrams

System --> DB : store project & tasks
DB --> System : retrieve tasks & progress

note right of System
  Project: {project.goal[:50]}{"..." if len(project.goal) > 50 else ""}
  Status: {project.status.capitalize()}
  Risk: {project.risk_level.capitalize()}
  Completion: {round(project.completion_rate)}%
end note

@enduml"""

    url = plantuml_url(code)
    return {
        "image_url": url,
        "image_path": None,
        "plantuml_code": code,
    }