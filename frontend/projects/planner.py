import json
import logging
import os

logger = logging.getLogger(__name__)

USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() in ("1", "true", "yes")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


def _prompt(goal: str, total_days: int) -> str:
    return f"""
You are an expert software manager.

Break this goal into structured development tasks.

Goal:{goal}
Total Days:{total_days}

Return ONLY valid JSON like this:
[
  {{
    "title": "",
    "description": "",
    "priority": "low/medium/high",
    "estimated_days": number
  }}
]
"""


def _parse_tasks(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("[")
        end = text.rfind("]") + 1
        return json.loads(text[start:end])


def generate_tasks(goal, total_days):
    """Generate a task list using Ollama.

    This function assumes Ollama is available and configured.
    If Ollama fails, it returns a fallback task.
    """

    if not USE_OLLAMA:
        logger.warning("USE_OLLAMA is not set to true. Task generation will use fallback.")
        return [
            {
                "title": "(Ollama not enabled)",
                "description": "Set USE_OLLAMA=true to enable task generation.",
                "priority": "high",
                "estimated_days": 1,
            }
        ]

    prompt = _prompt(goal, total_days)

    try:
        import ollama

        logger.info(f"Generating tasks using Ollama model: {OLLAMA_MODEL}")
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response["message"]["content"]
        logger.debug(f"Ollama response: {content}")

        tasks = _parse_tasks(content)
        if isinstance(tasks, list) and tasks:
            logger.info(f"Successfully generated {len(tasks)} tasks")
            return tasks
        else:
            logger.error("Ollama returned invalid task format")
            raise ValueError("Invalid task format")

    except Exception as e:
        logger.exception(f"Ollama task generation failed: {e}")
        return [
            {
                "title": "(Ollama task generation failed)",
                "description": f"Error: {str(e)}. Check Ollama is running and accessible.",
                "priority": "high",
                "estimated_days": 1,
            }
        ]


