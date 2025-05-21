from django.db import models

# from django.db.models.enums import Choices
from django.conf import settings

# from django.forms import ImageField
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser

# from django.core.exceptions import ValidationError

from .managers import CustomUserManager


class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    # Which campus user is located in.
    class Campus(models.TextChoices):
        BROWNSVILLE = "brownsville", "Brownsville"
        EDINBRUG = "edinburg", "Edinburg"

    # What type of user: students and advisor
    class UserTypes(models.TextChoices):
        STUDENT = "student", "Student"
        ADVISOR = "advisor", "Advisor"

    username = None
    email = models.EmailField(_("email"), unique=True)
    # make unique identifier into the email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    user_type = models.CharField(
        max_length=15, choices=UserTypes, default=UserTypes.STUDENT
    )
    campus = models.CharField(max_length=15, choices=Campus, default=Campus.BROWNSVILLE)
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField("Skill", blank=True)

    objects = CustomUserManager()  # pyright: ignore

    def __str__(self):
        return self.email


# Any additional advisor exclusive information
class AdvisorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    courses_taught = models.TextField()
    title = models.CharField(max_length=40)

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.user.email


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return self.user.email


class Project(models.Model):
    class Meta:
        # Permissions:
        # https://docs.djangoproject.com/en/5.2/topics/auth/default/#programmatically-creating-permissions
        # https://www.youtube.com/watch?v=AR5hjQ8nla0 |> Django Permissions | Model Level | Views and Templates
        # https://docs.djangoproject.com/en/5.2/topics/auth/default/#proxy-models
        # Custom permission for proposing projects into the database:
        permissions = (("can_propose_project", "Can Propose Project"),)

    # https://docs.djangoproject.com/en/5.2/ref/models/fields/#enumeration-types
    class Statuses(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        ARCHIVED = "archived", "Archived"
        TRASH = "trash", "Trash"

    title = models.CharField(max_length=40)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=Statuses, default=Statuses.PENDING)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_project",
    )
    member_limit = models.IntegerField(
        choices=[(2, "2"), (3, "3"), (4, "4")], default=4  # Only allow 2, 3, or 4
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="project_memberships",
        limit_choices_to={"user_type": User.UserTypes.STUDENT},
        blank=True,
    )
    advisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="advised_projects",
        limit_choices_to={"user_type": User.UserTypes.ADVISOR},
    )
    skills_required = models.ManyToManyField(Skill, blank=True)

    @property
    def applicants(self):
        return User.objects.filter(project_applications__project=self)

    # For cli purposes
    def __str__(self):
        return self.title


class ProjectApplication(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="applications"
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_applications",
        limit_choices_to={"user_type": User.UserTypes.STUDENT},
    )
    message = models.TextField(help_text="Tell us why you'd like to join this project")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "applicant")
        ordering = ["-applied_at"]

    def __str__(self):
        return f"Application by {self.applicant.email} to {self.project.title}"


# This is a way to allow the user to have the ability to favorite a project :^D.
class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites"
    )
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="favorites"
    )

    class Meta:
        unique_together = ("user", "project")

    def __str__(self):
        return f"{self.user} favorite {self.project}"


# https://testdriven.io/blog/django-custom-user-model/
