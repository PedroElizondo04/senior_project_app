from django.contrib import admin
from .models import (
    Project,
    User,
    Skill,
    ProjectApplication,
    AdvisorProfile,
    StudentProfile,
)

admin.site.register(Project)
admin.site.register(User)
admin.site.register(Skill)
admin.site.register(AdvisorProfile)
admin.site.register(StudentProfile)
admin.site.register(ProjectApplication)

# Register your models here.
