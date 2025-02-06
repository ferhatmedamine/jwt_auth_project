from django.db import models
from organisation.models import Organisation  # Import Organisation model

class Integration(models.Model):
    id = models.BigAutoField(primary_key=True)  # Automatically generated large integer ID
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="integrations")
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} (v{self.version}) - {'Enabled' if self.enabled else 'Disabled'}"
