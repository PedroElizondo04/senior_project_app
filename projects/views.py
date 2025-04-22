# projects/views.py

from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.exceptions import ValidationError

from .models import Advisor, Student
from .services import (
    get_user_role,
    get_visible_projects_for_user,
    can_student_create_project,
    validate_member_limit,
    create_project_with_author,
    attach_skills_to_project,
    link_project_to_creator,
    create_user_account,
)

# -------------------------------
# LOGIN PAGE
# -------------------------------
def loginPage(request):
    """Login view for all users"""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("landing")
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, "projects/loginPage.html")


# -------------------------------
# LANDING PAGE
# -------------------------------
@login_required(login_url="login")
def landingPage(request):
    """Landing page with actions based on user role"""
    role = get_user_role(request.user)
    return render(request, "projects/landingPage.html", {"role": role, "user": request.user})


# -------------------------------
# PROJECT LIST PAGE
# -------------------------------
@login_required(login_url="login")
def projectListPage(request):
    """List of projects visible to the current user"""
    role = get_user_role(request.user)
    projects = get_visible_projects_for_user(request.user)
    return render(request, "projects/projectListPage.html", {"projects": projects, "role": role})


# -------------------------------
# PROJECT PROPOSAL (CREATE)
# -------------------------------
@login_required(login_url="login")
def projectProposalPage(request):
    """Create a project as student, advisor, or admin"""
    role = get_user_role(request.user)

    if role not in ["STUDENT", "ADVISOR", "ADMIN"]:
        return HttpResponseForbidden("Only students, advisors or admins can create projects.")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        skills_input = request.POST.get("skills", "")
        member_limit = int(request.POST.get("member_limit", 4))

        if not validate_member_limit(member_limit):
            messages.error(request, "Member limit must be between 2 and 4.")
            return redirect("projectProposalPage")

        if role == "STUDENT":
            student = get_object_or_404(Student, user=request.user)
            if not can_student_create_project(student):
                messages.error(request, "You can only create one project.")
                return redirect("projectListPage")

        # Create and configure project
        project = create_project_with_author(title, description, member_limit, request.user, role)
        attach_skills_to_project(project, skills_input)
        link_project_to_creator(project, request.user, role)

        project.update_status()
        return redirect("projectListPage")

    return render(request, "projects/projectProposalPage.html", {"role": role})


# -------------------------------
# PROJECT DETAIL PAGE
# -------------------------------
@login_required(login_url="login")
def projectViewPage(request, project_id):
    """View an individual project’s info"""
    from .models import Project
    role = get_user_role(request.user)
    project = get_object_or_404(Project, id=project_id)
    return render(request, "projects/projectViewPage.html", {"project": project, "role": role})


# -------------------------------
# ADVISOR LIST
# -------------------------------
@login_required(login_url="login")
def advisorListPage(request):
    """View all advisors"""
    role = get_user_role(request.user)
    advisors = Advisor.objects.all()
    return render(request, "projects/advisorListPage.html", {"advisors": advisors, "role": role})


# -------------------------------
# ADVISOR PROFILE VIEW
# -------------------------------
@login_required(login_url="login")
def advisorProfileViewPage(request, name):
    """View an individual advisor"""
    role = get_user_role(request.user)
    advisor = get_object_or_404(Advisor, user__username=name)
    return render(request, "projects/advisorProfileViewPage.html", {"advisor": advisor, "role": role})


# -------------------------------
# STUDENT LIST (For advisors/admins)
# -------------------------------
@login_required(login_url="login")
def studentListPage(request):
    """Visible only to advisors and admins"""
    role = get_user_role(request.user)
    if role not in ["ADVISOR", "ADMIN"]:
        return HttpResponseForbidden("Only advisors and admins can view students.")

    students = Student.objects.all()
    return render(request, "projects/studentListPage.html", {"students": students, "role": role})


# -------------------------------
# CREATE ACCOUNT PAGE (Admin-only)
# -------------------------------
@login_required(login_url="login")
def createAccountPage(request):
    """Allow an admin to manually create a user account"""
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only admins can create user accounts.")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        try:
            user, created = create_user_account(username, password, email)
            if created:
                messages.success(request, f"User '{username}' created successfully.")
            else:
                messages.info(request, f"User '{username}' already exists.")
        except ValidationError as e:
            messages.error(request, str(e))
        return redirect("landing")

    return render(request, "projects/createAccountPage.html")
