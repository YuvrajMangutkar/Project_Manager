import os
from django.conf import settings
from groq import Groq
import logging

logger = logging.getLogger(__name__)

def generate_executive_summary(project, tasks):
    """
    Asks Groq to write a formal executive summary of the project's health.
    """
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY", settings.GROQ_API_KEY))
        
        total = tasks.count()
        completed = tasks.filter(status='completed').count()
        overdue = tasks.filter(status='overdue').count()
        
        prompt = f"""You are generating an Executive Summary Status Report for a project management dashboard.
        
Project Name: {project.goal}
Total Days: {project.total_days}
Overall Status: {project.status}
Completion Rate: {project.completion_rate}%
Total Tasks: {total}
Tasks Completed: {completed}
Tasks Overdue: {overdue}

Write a professional, 2-3 paragraph executive summary of the project's current health.
Do NOT use markdown. Write plain text only, separated by newlines. Be analytical and professional."""

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500,
        )
        
        return completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Failed to generate executive summary: {str(e)}")
        return "Executive summary is currently unavailable due to an AI processing error."
