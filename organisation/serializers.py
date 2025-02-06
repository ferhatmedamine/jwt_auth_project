from rest_framework import serializers
from .models import Organisation
from django.contrib.auth import get_user_model

User = get_user_model()

class OrganisationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)  # Ensure user is included

    class Meta:
        model = Organisation
        fields = ['id', 'name', 'domain', 'user']  # Include 'user' in the fields
