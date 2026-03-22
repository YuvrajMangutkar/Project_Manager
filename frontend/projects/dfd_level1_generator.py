from .plantuml_encoder import plantuml_url
from .models import Task, AIInsight


def generate_dfd_level1(project):
    """
    DFD Level 1 (Internal Agents) via PlantUML public server.
    - Dark theme skinparams
    - Shows real task counts and insight counts per agent
    - Highlights active agents based on project data
    """
    tasks = Task.objects.filter(project=project)
    total_tasks     = tasks.count()
    completed_tasks = tasks.filter(status="completed").count()
    pending_tasks   = tasks.filter(status="pending").count()
    overdue_tasks   = tasks.filter(status="in_progress").count()

    planner_insights  = AIInsight.objects.filter(project=project, agent_type="planner").count()
    analyzer_insights = AIInsight.objects.filter(project=project, agent_type="analyzer").count()
    optimizer_insights = AIInsight.objects.filter(project=project, agent_type="optimizer").count()

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
skinparam CircleBorderColor #10B981
skinparam CircleBackgroundColor #064E3B
skinparam CircleFontColor #F1F5F9
skinparam DatabaseBorderColor #F59E0B
skinparam DatabaseBackgroundColor #1C1917
skinparam DatabaseFontColor #F59E0B
skinparam NoteBackgroundColor #1E293B
skinparam NoteBorderColor #475569
skinparam NoteFontColor #94A3B8

rectangle "👤 User" as User #1E3A5F

circle "🧠 Planner Agent\\n({planner_insights} insight(s))" as P1
circle "📅 Scheduler Agent\\n({total_tasks} task(s) created)" as P2
circle "🔍 Critic Agent\\n({analyzer_insights} insight(s))" as P3
circle "👁️ Monitor Agent\\n({optimizer_insights} insight(s))" as P4
circle "📐 Diagram Generator\\n(4 diagram types)" as P5

database "🗄️ Project Database\\n({completed_tasks} done | {pending_tasks} pending)" as DB

User --> P1 : project goal + {project.total_days} day(s)

P1 --> P2 : {total_tasks} generated task(s)

P2 --> DB : store scheduled tasks & due dates
DB --> P3 : retrieve task & progress data

P3 --> P4 : health analysis\\n(Risk: {project.risk_level.capitalize()})

P4 --> P5 : {planner_insights + analyzer_insights + optimizer_insights} insight(s) & alerts

P5 --> User : use case, activity, DFD diagrams

note right of P1
  Status: {project.status.capitalize()}
  Completion: {round(project.completion_rate)}%
  Delayed tasks: {project.delayed_tasks}
end note

note right of DB
  Total Tasks: {total_tasks}
  Completed:   {completed_tasks}
  Pending:     {pending_tasks}
  In Progress: {overdue_tasks}
end note

@enduml"""

    url = plantuml_url(code)
    return {
        "image_url": url,
        "image_path": None,
        "plantuml_code": code,
    }