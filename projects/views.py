from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.utils.timezone import now
from .models import Project, Skill, Advisor, Student, ProjectApplication, AdvisorApplication


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("landing")

    if request.method == "POST":
        email = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
            authenticated_user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            authenticated_user = None

        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect("landing")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "projects/loginPage.html")


@login_required(login_url="login")
def landingPage(request):
    role = get_user_role(request.user)
    context = {"role": role}
    return render(request, "projects/landingPage.html", context)


@login_required(login_url="login")
def projectViewPage(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    role = get_user_role(request.user)
    context = {"project": project, "role": role}
    return render(request, "projects/projectViewPage.html", context)


@login_required(login_url="login")
def advisorListPage(request):
    role = get_user_role(request.user)
    advisors = Advisor.objects.all()
    context = {"advisors": advisors, "role": role}
    return render(request, "projects/advisorListPage.html", context)


@login_required(login_url="login")
def advisorProfileViewPage(request, name):
    role = get_user_role(request.user)
    advisor = get_object_or_404(Advisor, user__username=name)
    context = {"advisor": advisor, "role": role}
    return render(request, "projects/advisorProfileViewPage.html", context)


@login_required(login_url="login")
def projectListPage(request):
    role = get_user_role(request.user)
    projects = Project.objects.all()
    context = {"projects": projects, "role": role}
    return render(request, "projects/projectListPage.html", context)


@login_required(login_url="login")
def projectProposalPage(request):
    role = get_user_role(request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        skills_input = request.POST.get("skills", "")
        member_limit = int(request.POST.get("member_limit", 4))

        student = get_object_or_404(Student, user=request.user)

        project = Project.objects.create(
            title=title,
            description=description,
            member_limit=member_limit,
            status="in_process",
            created_at=now()
        )

        # Link student as creator
        student.created_project = project
        student.save()

        # Handle comma-separated skills
        skill_names = [s.strip() for s in skills_input.split(",") if s.strip()]
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name)
            project.skills_required.add(skill)

        project.save()
        return redirect("projectListPage")

    return render(request, "projects/projectProposalPage.html", {"role": role})


def get_user_role(user):
    if user.is_superuser:
        return "ADMIN"
    elif hasattr(user, 'student'):
        return "STUDENT"
    elif hasattr(user, 'advisor'):
        return "ADVISOR"
    return "UNKNOWN"
