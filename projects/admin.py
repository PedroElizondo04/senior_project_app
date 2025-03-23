from django.contrib import admin

# Register your models here.
from .models import Project, Student, Advisor, ProjectApplication, Skill

admin.site.register(Project)
admin.site.register(Student)
admin.site.register(Advisor)
admin.site.register(ProjectApplication)
admin.site.register(Skill)