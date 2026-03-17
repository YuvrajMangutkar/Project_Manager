from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import AIInsight

@receiver(post_save, sender=AIInsight)
def send_notification_on_critical_event(sender,instance, created,**kwargs):
    if not created:
        return 
    
    project= instance.project

    if instance.agent_type in ['scheduler','monitor'] or project.risk_level=="High":
        send_mail(
            subject=f"⚠ Project Alert: {project.goal}",
            message=(
                f"Project Status: {project.status}\n"
                f"Risk Level: {project.risk_level}\n\n"
                f"Insight:\n{instance.message}"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[project.user.email],
            fail_silently=True,
        )
