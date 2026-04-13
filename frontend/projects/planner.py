import json
import logging
import os

logger = logging.getLogger(__name__)

# ── Provider selection ──────────────────────────────────────────────────────
# Priority: Groq → Ollama → Fallback task
#
# Groq (FREE, Llama3 model, works on Render):
#   Set GROQ_API_KEY in your Render environment variables.
#   Get a free key at https://console.groq.com
#
# Ollama (self-hosted):
#   Set USE_OLLAMA=true and OLLAMA_HOST=http://<your-ollama-service-url>:11434
#   You can run Ollama as a separate Docker service on Render.

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")  # free model on Groq

USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() in ("1", "true", "yes")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_HOST = os.getenv("OLLAMA_HOST")


def _prompt(goal: str, total_days: int) -> str:
    return f"""You are an expert software project manager.
Break this software development goal into structured tasks.

Goal: {goal}
Total Days: {total_days}

Return ONLY valid JSON — no markdown, no explanation, no code fences. Example:
[
  {{
    "title": "Task title",
    "description": "Short description",
    "priority": "medium",
    "estimated_days": 2
  }}
]

Rules:
- priority must be one of: low, medium, high
- estimated_days must be a positive integer
- Return ONLY the JSON array, nothing else
"""


def _parse_tasks(text: str):
    """Parse JSON from LLM response, stripping markdown fences if present."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        end = -1 if lines[-1].strip() == "```" else len(lines)
        text = "\n".join(lines[1:end])
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("[")
        end = text.rfind("]") + 1
        if start != -1 and end > start:
            return json.loads(text[start:end])
        raise


def _fallback_tasks(reason: str):
    return [
        {
            "title": "Configure AI Task Generation",
            "description": (
                f"AI task generation is not available: {reason}. "
                "To enable it, set GROQ_API_KEY (free at console.groq.com) "
                "or set USE_OLLAMA=true with OLLAMA_HOST pointing to your Ollama server. "
                "You can also add tasks manually from the dashboard."
            ),
            "priority": "high",
            "estimated_days": 1,
        }
    ]


def _generate_with_groq(goal: str, total_days: int):
    """
    Generate tasks using Groq's free Llama3 API.
    Groq is OpenAI-compatible — uses the same openai library.
    """
    from openai import OpenAI

    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    )
    prompt = _prompt(goal, total_days)
    logger.info(f"Generating tasks via Groq (model={GROQ_MODEL})")

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    content = response.choices[0].message.content
    logger.debug(f"Groq response: {content}")

    tasks = _parse_tasks(content)
    if isinstance(tasks, list) and tasks:
        logger.info(f"Groq generated {len(tasks)} tasks successfully")
        return tasks
    raise ValueError("Groq returned empty or invalid task list")


def _generate_with_ollama(goal: str, total_days: int):
    """Generate tasks using Ollama (local or self-hosted)."""
    import ollama

    client = ollama.Client(host=OLLAMA_HOST)
    prompt = _prompt(goal, total_days)
    logger.info(f"Generating tasks via Ollama (model={OLLAMA_MODEL}, host={OLLAMA_HOST})")

    response = client.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"timeout": 30}
    )
    content = response["message"]["content"]
    logger.debug(f"Ollama response: {content}")

    tasks = _parse_tasks(content)
    if isinstance(tasks, list) and tasks:
        logger.info(f"Ollama generated {len(tasks)} tasks successfully")
        return tasks
    raise ValueError("Ollama returned empty or invalid task list")


def generate_tasks(goal: str, total_days: int):
    """
    Generate tasks from a project goal.

    Provider priority:
      1. Groq   — free Llama3 API (set GROQ_API_KEY)
      2. Ollama — self-hosted     (set USE_OLLAMA=true + OLLAMA_HOST)
      3. Fallback informational task
    """

    # 1. Try Groq (recommended for production — free & fast)
    if GROQ_API_KEY:
        try:
            return _generate_with_groq(goal, total_days)
        except Exception as e:
            logger.warning(f"Groq failed: {e}. Trying Ollama...")

    # 2. Try Ollama (works when OLLAMA_HOST points to a running server)
    if USE_OLLAMA and OLLAMA_HOST and OLLAMA_HOST != "http://localhost:11434":
        try:
            return _generate_with_ollama(goal, total_days)
        except Exception as e:
            logger.warning(f"Ollama failed: {e}. Returning fallback task.")

    # 3. Nothing configured or all failed
    if not GROQ_API_KEY and not (USE_OLLAMA and OLLAMA_HOST and OLLAMA_HOST != "http://localhost:11434"):
        reason = "No AI provider configured. Set GROQ_API_KEY (free at console.groq.com) or set USE_OLLAMA=true with OLLAMA_HOST pointing to your Ollama server."
    else:
        reason = "All configured AI providers failed — check build logs."

    logger.error(f"Task generation fallback triggered: {reason}")
    return _fallback_tasks(reason)
