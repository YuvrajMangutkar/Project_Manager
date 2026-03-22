from .plantuml_encoder import plantuml_url
from .models import Task


def generate_activity_diagram(project):
    """Activity Diagram via PlantUML public server."""
    tasks = Task.objects.filter(project=project).order_by("id")

    code = "@startuml\n"
    code += "skinparam backgroundColor #FAFAFA\n"
    code += "start\n"
    code += ":Create Project;\n"
    code += ":Generate Task Plan;\n"

    for task in tasks:
        safe_title = (
            task.title
            .replace("(", "")
            .replace(")", "")
            .replace('"', "")
            .strip()
        )
        code += f":{safe_title};\n"

    code += ":Analyze Project Health;\n"
    code += ":Generate Diagrams;\n"
    code += "stop\n"
    code += "@enduml"

    url = plantuml_url(code)
    return {
        "image_url": url,
        "image_path": None,
        "plantuml_code": code,
    }