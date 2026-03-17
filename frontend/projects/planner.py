import ollama 
import json

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
    response=ollama.chat(
        model="llama3",
        messages=[
            {"role":"user","content":prompt}

        ]
    )
    content=response['message']['content']
    #sometimes the model add the extra text -we have to clean it.
    try:
        tasks=json.loads(content)

    except:
        #fallback
        start=content.find('[')
        end=content.rfind(']')+1
        tasks=json.loads(content[start:end])
    return tasks

