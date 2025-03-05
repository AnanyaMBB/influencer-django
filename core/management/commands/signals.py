from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.utils.timezone import now
from ...models import PhylloScheduledPost
from django.core.management import call_command

@receiver(post_save, sender=PhylloScheduledPost)
def handle_new_post(sender, instance, created, **kwargs):
    if created and instance.scheduled_time > now():
        call_command("scheduler")  # Starts scheduler if not running

        # 🔥 Import Command inside the function to prevent circular import
        from core.management.commands.scheduler import Command  
        
        scheduler = Command()  # Create an instance of the scheduler
        scheduler.add_job_to_scheduler(instance)  # Add job to scheduler
