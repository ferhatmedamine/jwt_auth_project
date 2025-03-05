from django.contrib.auth.models import AbstractUser
from django.db import models
from organisation.models import Organisation  # Import Organisation model

class OrganisationRole(models.TextChoices):
    ADMIN = "admin", "Organisation Admin"
    STAFF = "staff", "Organisation Staff"
    USER = "user", "Organisation User"

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'User'),
    ]
    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, related_name="users")  # 🔥 Use string reference
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def is_admin(self):
        return self.role == 'admin'

    def is_staff(self):
        return self.role == 'staff'

    def is_user(self):
        return self.role == 'user'

    @property
    def is_superuser(self):
        return self.role == 'admin'

    @property
    def is_staff(self):
        return self.role in ['admin', 'staff']
