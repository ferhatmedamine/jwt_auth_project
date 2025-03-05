from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserRole

@receiver(post_save, sender=UserRole)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        print(f"Sending welcome email to {instance.user.email} for {instance.organisation.name}")