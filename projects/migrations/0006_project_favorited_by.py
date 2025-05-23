# Generated by Django 5.2 on 2025-05-06 19:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0005_alter_project_author_id_alter_project_author_type"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="favorited_by",
            field=models.ManyToManyField(
                blank=True,
                related_name="favorite_projects",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
