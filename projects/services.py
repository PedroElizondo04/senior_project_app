# projects/services.py

from .models import Project, Skill, Student, Advisor
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

# -------------------------------
# Determine user role from Django user instance
# -------------------------------
def get_user_role(user):
    """Returns the role name based on user type"""
    if user.is_superuser:
        return "ADMIN"
    elif hasattr(user, 'student'):
        return "STUDENT"
    elif hasattr(user, 'advisor'):
        return "ADVISOR"
    return "UNKNOWN"


# -------------------------------
# Filter visible projects per user role
# -------------------------------
def get_visible_projects_for_user(user):
    """Admins see all; others only see active/in_process"""
    if user.is_superuser:
        return Project.objects.all()
    return Project.objects.filter(status__in=["active", "in_process"])


# -------------------------------
# Check if student can create a project
# -------------------------------
def can_student_create_project(student):
    """Only allow one project per student"""
    return student.created_project is None


# -------------------------------
# Validate member limit for a project
# -------------------------------
def validate_member_limit(limit):
    """Only allow member limits between 2–4"""
    return 2 <= limit <= 4


# -------------------------------
# Create project with author (student or advisor)
# -------------------------------
def create_project_with_author(title, description, member_limit, user, role):
    """Creates a project with proper content type for the author"""
    model_class = Student if role == "STUDENT" else Advisor
    content_type = ContentType.objects.get_for_model(model_class)

    project = Project.objects.create(
        title=title,
        description=description,
        member_limit=member_limit,
        status="in_process",
        created_at=now(),
        author_type=content_type,
        author_id=user.id
    )
    return project


# -------------------------------
# Attach comma-separated skills to project
# -------------------------------
def attach_skills_to_project(project, skills_input):
    """Adds skills to a project (creates them if needed)"""
    skill_names = [s.strip() for s in skills_input.split(",") if s.strip()]
    for name in skill_names:
        skill, _ = Skill.objects.get_or_create(name=name)
        project.skills_required.add(skill)


# -------------------------------
# Link project to student or advisor
# -------------------------------
def link_project_to_creator(project, user, role):
    """Assigns the project to the creator depending on role"""
    if role == "STUDENT":
        student = get_object_or_404(Student, user=user)
        student.created_project = project
        student.save()
    elif role == "ADVISOR":
        advisor = get_object_or_404(Advisor, user=user)
        project.advisor = advisor
        project.save()
