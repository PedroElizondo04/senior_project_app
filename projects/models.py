from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = [
        ('in_process', 'In Process'),  # Not enough members or missing advisor
        ('active', 'Active'),          # Has full members AND advisor
        ('completed', 'Completed'),    # Fully completed
        ('archived', 'Archived'),      # Projects saved for next semesters
        ('trash', 'Trash'),            # Unwanted Student Projects
    ]

    author_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    author_id = models.PositiveIntegerField()
    author = GenericForeignKey('author_type', 'author_id')

    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.ManyToManyField(Skill, blank=True)
    member_limit = models.IntegerField(
        choices=[(2, "2"), (3, "3"), (4, "4")],
        default=4
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_process')
    created_at = models.DateTimeField(auto_now_add=True)
    advisor = models.ForeignKey("Advisor", on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    students = models.ManyToManyField("Student", blank=True)

    def update_status(self):
        student_count = self.students.count()
        has_advisor = self.advisor is not None

        # Active only if has advisor and full members
        if has_advisor and student_count == self.member_limit:
            self.status = 'active'
        else:
            self.status = 'in_process'

        self.save()

    def mark_as_trash(self):
        self.status = 'trash'
        self.save()

    def __str__(self):
        return f"{self.title} ({self.status})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_project = models.OneToOneField(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='creator')

    def apply_to_project(self, project, text):
        if not self.created_project and not ProjectApplication.objects.filter(student=self, status='accepted').exists():
            ProjectApplication.objects.create(student=self, project=project, application_text=text)

    def accept_application(self, application):
        application.status = "accepted"
        application.save()
        self.created_project = application.project
        self.save()
        ProjectApplication.objects.filter(student=self).exclude(id=application.id).update(status="nullified")
        if self.created_project:
            self.created_project.mark_as_trash()

    def __str__(self):
        return f"Student: {self.user.username}"

class Advisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='advisor_images/', blank=True, null=True)

    def apply_to_project(self, project):
        AdvisorApplication.objects.create(advisor=self, project=project)

    def __str__(self):
        return f"Advisor: {self.user.username}"

class ProjectApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('nullified', 'Nullified'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    application_text = models.TextField()  # REQUIRED field
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} -> {self.project.title} ({self.status})"

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
