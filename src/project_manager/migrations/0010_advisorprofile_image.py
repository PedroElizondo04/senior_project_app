# Generated by Django 5.2 on 2025-05-07 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0009_studentprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisorprofile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
