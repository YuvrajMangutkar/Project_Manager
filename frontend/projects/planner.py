import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_tasks(goal,total_days):
    prompt=f"""
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
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    #sometimes the model add the extra text -we have to clean it.
    try:
        tasks=json.loads(content)

    except:
        #fallback
        start=content.find('[')
        end=content.rfind(']')+1
        tasks=json.loads(content[start:end])
    return tasks

