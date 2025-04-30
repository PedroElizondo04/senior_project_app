from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
# Project model with different statuses
class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('in_process', 'In Process'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
        ('trash', 'Trash'),
    ]
    
    author_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    author_id = models.PositiveIntegerField()
    author = GenericForeignKey('author_type', 'author_id')
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.ManyToManyField(Skill, blank=True)
    member_limit = models.IntegerField(
        choices=[(2, "2"), (3, "3"), (4, "4")],  # Only allow 2, 3, or 4
        default=4
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_process')
    created_at = models.DateTimeField(auto_now_add=True)

    students = models.ManyToManyField("Student", blank=True)
    advisor = models.ForeignKey("Advisor", on_delete=models.SET_NULL, null=True, related_name="projects")  # One-to-Many relationship
    
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
    image = models.ImageField(upload_to='advisor_images/', blank=True, null=True)  # Uploads images to MEDIA_ROOT/advisor_images

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

def get_user_role(user):
    """Function to return the role of the user"""
    if user.is_superuser:
        return "Admin"
    elif hasattr(user, 'student'):
        return "Student"
    elif hasattr(user, 'advisor'):
        return "Advisor"
    return "UNKNOWN"
