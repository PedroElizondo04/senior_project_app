from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Project model with different statuses
class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('in_process', 'In Process'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
        ('trash', 'Trash'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.TextField()
    member_limit = models.IntegerField(default=4)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    advisor = models.ForeignKey("Advisor", on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField("Student", blank=True)
    
    def update_status(self):
        """ Updates project status based on members and advisor """
        if self.students.count() < 2 and not self.advisor:
            self.status = 'in_process'  # Still forming a group

        elif self.students.count() >= 2 and self.advisor:
            if self.students.count() == self.member_limit:
                self.status = 'active'  # Fully formed team with advisor
            else:
                self.status = 'in_process'  # Has advisor but not full team
        self.save()
    
    def __str__(self):
        return self.title

# Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_project = models.OneToOneField(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='creator')
    
    def apply_to_project(self, project):
        """ Students apply to a project """
        if not self.created_project and not ProjectApplication.objects.filter(student=self, status='accepted').exists():
            ProjectApplication.objects.create(student=self, project=project)
    
    def accept_application(self, application):
        """ Accept one application, nullify others """
        application.status = "accepted"
        application.save()
        self.created_project = application.project
        self.save()
        
        ProjectApplication.objects.filter(student=self).exclude(id=application.id).update(status="nullified")
    
        if self.created_project:
            self.created_project.mark_as_trash()

    def __str__(self):
        return self.user.username

# Advisor model
class Advisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    
    def apply_to_project(self, project):
        """ Advisors apply to be part of a student project """
        AdvisorApplication.objects.create(advisor=self, project=project)
    
    def __str__(self):
        return self.user.username

# Project applications
class ProjectApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('nullified', 'Nullified'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    application_text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.username} -> {self.project.title} ({self.status})"

# Advisor applications
class AdvisorApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.advisor.user.username} -> {self.project.title} ({self.status})"
