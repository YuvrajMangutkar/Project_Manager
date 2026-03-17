import json
import logging
import os

import openai

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_tasks(goal, total_days):
    """Generate a task list using OpenAI.

    If the OpenAI key is missing or the model response cannot be parsed, this
    returns a simple placeholder task so the project creation still works.
    """

    if not openai.api_key:
        logger.error("OPENAI_API_KEY is not set. Tasks cannot be generated.")
        return [
            {
                "title": "Configure OpenAI API key",
                "description": "Set OPENAI_API_KEY in your environment variables.",
                "priority": "high",
                "estimated_days": 1,
            }
        ]

    prompt = f"""
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

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400,
        )

        content = response.choices[0].message.content

        try:
            tasks = json.loads(content)
        except json.JSONDecodeError:
            # Fallback: attempt to extract JSON array from any surrounding text
            start = content.find("[")
            end = content.rfind("]") + 1
            tasks = json.loads(content[start:end])

        if not isinstance(tasks, list):
            raise ValueError("Expected a list of tasks")

        return tasks

    except Exception as e:
        logger.exception("Failed to generate tasks via OpenAI")
        return [
            {
                "title": "(AI task generation failed)",
                "description": (
                    "The AI task generator failed. "
                    "Check that OPENAI_API_KEY is set and valid. "
                    "See logs for details."
                ),
                "priority": "high",
                "estimated_days": 1,
            }
        ]


