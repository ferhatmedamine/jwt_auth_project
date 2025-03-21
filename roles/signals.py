from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Profile

@receiver(post_save, sender=Profile)
def assign_group(sender, instance, created, **kwargs):
    if created:
        group_name = None
        if instance.role == 'org_admin':
            group_name = 'org_admin'
        elif instance.role == 'org_staff':
            group_name = 'org_staff'
        elif instance.role == 'org_user':
            group_name = 'org_user'

        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            instance.user.groups.add(group)