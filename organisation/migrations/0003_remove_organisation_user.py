# Generated by Django 5.1.5 on 2025-02-06 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0002_organisation_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='user',
        ),
    ]
