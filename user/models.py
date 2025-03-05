from django.db import models
from django.contrib.auth.models import User
from organisation.models import Organisation
from .managers import UserRoleManager  # Import the custom manager

class UserRole(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
        ('editor', 'Editor'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='user_roles')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='student')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use the custom manager
    objects = UserRoleManager()

    def __str__(self):
        return f"{self.user.username} - {self.organisation.name} ({self.role})"

    class Meta:
        unique_together = ('user', 'organisation')  # Ensure a user can only have one role per organisation