from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
# from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Project, Advisor, Student, ProjectApplication, AdvisorApplication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def loginPage(request):
    """
    The login page for all users.
    Handles login authentication.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("landing")  # Redirect to landing page
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "projects/loginPage.html")

@login_required(login_url="login")
def landingPage(request):
    """
    The landing page for all users. Contains big action buttons depending on the role.
    """
    role = get_user_role(request.user)
    
    context = {
        "role": role,
        "user": request.user  # Explicitly passing user
    }
    return render(request, "projects/landingPage.html", context)

@login_required(login_url="login")
def projectViewPage(request, project_id):
    """
    The view page of a project to see its author, description, skills, etc.
    """
    project = get_object_or_404(Project, id=project_id)
    role = get_user_role(request.user)
    
    context = {"project": project, "role": role}
    return render(request, "projects/projectViewPage.html", context)

@login_required(login_url="login")
def advisorListPage(request):
    """
    View a list of advisors and their contact information. 
    """
    role = get_user_role(request.user)
    
    advisors = Advisor.objects.all()
    context = {"advisors": advisors, "role": role}
    return render(request, "projects/advisorListPage.html", context)

@login_required(login_url="login")
def advisorProfileViewPage(request, name):
    """
    View an individual advisor and their contact information.
    """
    role = get_user_role(request.user)

    advisor = get_object_or_404(Advisor, user__username=name)
    context = {"advisor": advisor, "role": role}
    return render(request, "projects/advisorProfileViewPage.html", context)

@login_required(login_url="login")
def projectListPage(request):
    """
    The list page for projects, contains a table of projects and the ability to filter, apply, etc.
    """
    role = get_user_role(request.user)
    projects = Project.objects.all()

    context = {"projects": projects, "role": role}
    return render(request, "projects/projectListPage.html", context)

@login_required(login_url="login")
def projectProposalPage(request):
    """
    The page to create the project proposal to convince others to join.
    """
    role = get_user_role(request.user)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        student = get_object_or_404(Student, user=request.user)
        
        project = Project.objects.create(
            title=title, 
            description=description, 
            created_at=now()
        )
        student.created_project = project
        student.save()
        return redirect('projectListPage')  # Redirect to the project list after submission

    return render(request, "projects/projectProposalPage.html", {"role": role})

@login_required(login_url="login")
def studentListPage(request):
    return

def get_user_role(user):
    if user.is_superuser:
        return "ADMIN"
    elif hasattr(user, 'student'):
        return "STUDENT"
    elif hasattr(user, 'advisor'):
        return "ADVISOR"
    return "UNKNOWN"