from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

# Custom User model with role-based access
class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('advisor', 'Advisor'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    USERNAME_FIELD = 'email'  # Use email as login field
    REQUIRED_FIELDS = ['username']  # Keep username for compatibility
    
    def __str__(self):
        return f"{self.email} ({self.role})"

# Project model with different statuses
class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('in_process', 'In Process'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
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
        if self.students.count() >= 2 and self.advisor:
            self.status = 'in_process'
        if self.students.count() == self.member_limit and self.advisor:
            self.status = 'completed'
        self.save()
    
    def __str__(self):
        return self.title

# Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=100, blank=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    skills = models.TextField(blank=True)
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

# Admin model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
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
