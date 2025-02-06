from django.db import models

class Organisation(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)

    def __str__(self):
        return self.name
