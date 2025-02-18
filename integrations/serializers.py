from rest_framework import serializers
from .models import Integration, MoodleIntegration

class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = '__all__'

class MoodleIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodleIntegration
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Remove the polymorphic_ctype field
        representation.pop('polymorphic_ctype', None)
        return representation