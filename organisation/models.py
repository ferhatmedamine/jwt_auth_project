from django.db import models
from django.contrib.auth import get_user_model


class Organisation(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    user = models.ForeignKey('auth user', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
