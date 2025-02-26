from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, Student, Advisor, Admin, ProjectApplication

admin.site.register(Project)
admin.site.register(Student)
admin.site.register(Advisor)
admin.site.register(Admin)
admin.site.register(ProjectApplication)