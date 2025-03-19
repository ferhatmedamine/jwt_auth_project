from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Profile

@receiver(post_save, sender=Profile)
def assign_user_to_group(sender, instance, created, **kwargs):
    user = instance.user
    if instance.role == 'org_admin':
        group = Group.objects.get(name='org_admin')
    elif instance.role == 'org_staff':
        group = Group.objects.get(name='org_staff')
    else:
        group = Group.objects.get(name='org_user')
    
    user.groups.clear()  # Remove user from all groups
    user.groups.add(group)  # Add user to the appropriate group