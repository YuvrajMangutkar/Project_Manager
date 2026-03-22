from .plantuml_encoder import plantuml_url
from .models import Task


def generate_usecase_diagram(project):
    """Generate a Use Case diagram using the free PlantUML public server."""
    tasks = Task.objects.filter(project=project)

    code = "@startuml\n"
    code += "skinparam backgroundColor #FAFAFA\n"
    code += "actor User\n"
    code += f'rectangle "{project.goal}" {{\n\n'

    code += "  User --> (Create Project)\n"
    code += "  User --> (Track Tasks)\n"
    code += "  User --> (View Project Health)\n"
    code += "  User --> (Generate Diagrams)\n\n"
    code += "  (Track Tasks) --> (Complete Task)\n"
    code += "  (Track Tasks) --> (Update Progress)\n\n"

    for task in tasks:
        safe_title = (
            task.title
            .replace("(", "")
            .replace(")", "")
            .replace('"', "")
            .strip()
        )
        code += f'  (Track Tasks) ..> ({safe_title}) : <<include>>\n'

    code += "\n}\n@enduml"

    url = plantuml_url(code)
    return {
        "image_url": url,
        "image_path": None,   # no local file; download via URL
        "plantuml_code": code,
    }