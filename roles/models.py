from django.contrib.auth.models import User
from django.db import models

class Organisation(models.Model):
    name = models.CharField(max_length=255)
    # Add other fields for your organisation

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, blank=True)
    ROLE_CHOICES = [
        ('org_admin', 'Organization Admin'),
        ('org_staff', 'Organization Staff'),
        ('org_user', 'Organization User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='org_user')

    def __str__(self):
        return f"{self.user.username} - {self.role} - {self.organisation}"