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
    """Generate a task list.

    If USE_OLLAMA is true, try using Ollama (local or remote).
    Otherwise, fall back to OpenAI.

    If neither works, return a fallback placeholder task so the project
    creation still succeeds.
    """

    prompt = _prompt(goal, total_days)

    if USE_OLLAMA:
        try:
            import ollama

            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
            )
            content = response["message"]["content"]
            tasks = _parse_tasks(content)
            if isinstance(tasks, list):
                return tasks
        except Exception:
            logger.exception("Ollama task generation failed")

    # Final fallback (ensures we still create at least one task)
    return [
        {
            "title": "(AI task generation unavailable)",
            "description": (
                "The app could not generate tasks automatically. "
                "To enable task generation, set USE_OLLAMA=true and ensure Ollama is available."
            ),
            "priority": "high",
            "estimated_days": 1,
        }
    ]


