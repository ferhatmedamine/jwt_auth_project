# Generated by Django 5.1.5 on 2025-02-25 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0002_moodleintegration_alter_integration_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='moodleintegration',
            name='courses',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='moodleintegration',
            name='grades',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
