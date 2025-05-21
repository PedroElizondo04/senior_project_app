from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

from .models import Project, Skill, Advisor, Student, ProjectApplication, AdvisorApplication
from .services import (
    get_user_role,
    get_visible_projects_for_user,
    can_student_create_project,
    validate_member_limit,
    create_project_with_author,
    attach_skills_to_project,
    link_project_to_creator,
)

# -------------------------------
# LOGIN PAGE
# -------------------------------
def loginPage(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("landingPage")
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, "projects/loginPage.html")

# -------------------------------
# LOGOUT
# -------------------------------
@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect('login')

# -------------------------------
# BASE VIEW
# -------------------------------
def baseView(request):
    return render(request, "base.html")

# -------------------------------
# LANDING PAGE
# -------------------------------
@login_required(login_url="login")
def landingPage(request):
    role = get_user_role(request.user)
    created_project = None
    if role == "Student":
        try:
            student = Student.objects.get(user=request.user)
            created_project = student.created_project
        except Student.DoesNotExist:
            pass
    context = {
        "role": role,
        "user": request.user,
        "created_project": created_project,
    }
    return render(request, "projects/landingPage.html", context)

# -------------------------------
# PROJECT LIST PAGE
# -------------------------------
@login_required(login_url="login")
def projectListPage(request):
    user = request.user
    role = get_user_role(user)
    show_my_groups = request.GET.get('show_my_groups', 'false') == 'true'
    projects = Project.objects.all()

    if role == "Student":
        student = Student.objects.get(user=user)
        user_project = student.created_project
        if user_project:
            projects = [user_project] + [p for p in projects if p != user_project]

    elif role == "Advisor" and show_my_groups:
        advisor = Advisor.objects.get(user=user)
        projects = projects.filter(advisor=advisor)

    paginator = Paginator(projects, 15)
    page = request.GET.get('page', 1)
    projects_page = paginator.get_page(page)

    context = {
        "projects": projects_page,
        "role": role,
        "user": user,
        "total_projects": paginator.count,
        "current_page": projects_page.number,
        "total_pages": paginator.num_pages,
        "show_my_groups": show_my_groups,
        "toggle_button_url": f"?show_my_groups={'false' if show_my_groups else 'true'}",
    }
    return render(request, "projects/projectListPage.html", context)

# -------------------------------
# PROJECT PROPOSAL PAGE
# -------------------------------
@login_required(login_url="login")
def projectProposalPage(request, project_id=None):
    student = Student.objects.get(user=request.user)
    existing_project = get_object_or_404(Project, id=project_id) if project_id else student.created_project

    if existing_project:
        if request.method == "POST":
            existing_project.title = request.POST.get("title")
            existing_project.description = request.POST.get("description")
            existing_project.member_limit = int(request.POST.get("member_limit", 4))
            skills_input = request.POST.get("skills", "")
            skill_names = [s.strip() for s in skills_input.split(",") if s.strip()]
            existing_project.skills_required.clear()
            for name in skill_names:
                skill, _ = Skill.objects.get_or_create(name=name)
                existing_project.skills_required.add(skill)
            existing_project.save()
            return redirect("projectList")
        return render(request, "projects/projectProposalPage.html", {"existing_project": existing_project})

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        skills_input = request.POST.get("skills", "")
        member_limit = int(request.POST.get("member_limit", 4))

        project = Project.objects.create(
            title=title,
            description=description,
            member_limit=member_limit,
            status="in_process",
            author=request.user
        )
        student.created_project = project
        student.save()

        skill_names = [s.strip() for s in skills_input.split(",") if s.strip()]
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name)
            project.skills_required.add(skill)

        return redirect("projectList")

    return render(request, "projects/projectProposalPage.html")

# -------------------------------
# PROJECT DETAIL PAGE
# -------------------------------
@login_required(login_url="login")
def projectViewPage(request, project_id):
    role = get_user_role(request.user)
    project = get_object_or_404(Project, id=project_id)
    return render(request, "projects/projectViewPage.html", {"project": project, "role": role})

# -------------------------------
# ADVISOR LIST PAGE
# -------------------------------
@login_required(login_url="login")
def advisorListPage(request):
    role = get_user_role(request.user)
    advisors = Advisor.objects.all()
    return render(request, "projects/advisorListPage.html", {"advisors": advisors, "role": role})

# -------------------------------
# ADVISOR PROFILE VIEW PAGE
# -------------------------------
@login_required(login_url="login")
def advisorProfileViewPage(request, id):
    advisor = get_object_or_404(Advisor, id=id)
    role = get_user_role(request.user)
    return render(request, "projects/advisorProfileViewPage.html", {"advisor": advisor, "role": role})

# -------------------------------
# STUDENT LIST PAGE
# -------------------------------
@login_required(login_url="login")
def studentListPage(request):
    role = get_user_role(request.user)
    if role not in ["Advisor", "Admin"]:
        return HttpResponseForbidden("Only advisors and admins can view students.")
    students = Student.objects.all()
    return render(request, "projects/studentListPage.html", {"students": students, "role": role})

# -------------------------------
# TOGGLE FAVORITE (AJAX)
# -------------------------------
@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user

    if user in project.favorited_by.all():
        project.favorited_by.remove(user)
        favorited = False
    else:
        project.favorited_by.add(user)
        favorited = True

    return JsonResponse({'favorited': favorited})
