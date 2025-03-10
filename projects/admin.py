from django.contrib import admin

# Register your models here.
from .models import Project, Student, Advisor, ProjectApplication

admin.site.register(Project)
admin.site.register(Student)
admin.site.register(Advisor)
admin.site.register(ProjectApplication)
