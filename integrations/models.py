from django.db import models
from polymorphic.models import PolymorphicModel  # Import Organisation model
from organisation.models import Organisation

class Integration(PolymorphicModel):
    id = models.BigAutoField(primary_key=True)  # Automatically generated large integer ID
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="integrations")
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    

    def __str__(self):
        return f"{self.name} (v{self.version}) - {'Enabled' if self.enabled else 'Disabled'}"
    
class MoodleIntegration(Integration):
    moodle_url = models.URLField()  # URL of the Moodle instance
    api_key = models.CharField(max_length=255)  # API Key for Moodle authentication
    courses = models.JSONField(default=list, blank=True)  # Store course data
    grades = models.JSONField(default=list, blank=True)  # Store grades data

    def __str__(self):
        return f"Moodle Integration for {self.organisation.name}"
