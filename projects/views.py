from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Skill, Advisor, Student, ProjectApplication, AdvisorApplication
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from django.http import JsonResponse
from django.views.decorators.http import require_POST


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
            return redirect("landingPage")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "projects/loginPage.html")

@login_required(login_url="login")
def landingPage(request):
    """
    The landing page for all users. Contains big action buttons depending on the role.
    """
    role = get_user_role(request.user)  # Get the user's role

    # Only fetch the student if the logged-in user is a student
    if role == "Student":
        try:
            student = Student.objects.get(user=request.user)
            created_project = student.created_project
        except Student.DoesNotExist:
            created_project = None
    else:
        created_project = None

    context = {
        "role": role,  # Pass the role to the template
        "user": request.user,
        "created_project": created_project,  # Pass the created_project to the template
    }
    return render(request, "projects/landingPage.html", context)

@login_required(login_url="login")
def projectViewPage(request, project_id):
    """
    The view page of a project to see its author, description, skills, etc.
    """
    project = get_object_or_404(Project, id=project_id)
    context = {"project": project}
    return render(request, "projects/projectViewPage.html", context)

@login_required(login_url="login")
def advisorListPage(request):
    """
    View a list of advisors and their contact information. 
    """
    advisors = Advisor.objects.all()
    context = {"advisors": advisors}
    return render(request, "projects/advisorListPage.html", context)

@login_required(login_url="login")
def advisorProfileViewPage(request, id):
    """
    View an individual advisor and their contact information.
    """
    advisor = get_object_or_404(Advisor, id=id)
    role = get_user_role(request.user)  # Make sure role is passed dynamically
    context = {"advisor": advisor, "role": role}
    return render(request, "projects/advisorProfileViewPage.html", context)


@login_required(login_url="login")
def projectListPage(request):
    """
    The list page for projects, contains a table of projects and the ability to filter, apply, etc.
    """
    user = request.user
    role = get_user_role(user)

    # Flag to filter advisor's projects
    show_my_groups = request.GET.get('show_my_groups', 'false') == 'true'

    # Fetch all projects
    projects = Project.objects.all()

    if role == "Student":
        student = Student.objects.get(user=user)
        user_project = student.created_project
        if user_project:
            projects = [user_project] + [project for project in projects if project != user_project]

    elif role == "Advisor":
        if show_my_groups:
            # Show only projects where the advisor is assigned
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
        "toggle_button_url": f"?show_my_groups={'false' if show_my_groups else 'true'}",  # Added context for the button's URL
    }
    return render(request, "projects/projectListPage.html", context)



@login_required(login_url="login")
def projectProposalPage(request, project_id=None):
    """
    The page to create or edit a project proposal.
    """
    student = Student.objects.get(user=request.user)
    
    # Check if the user has a project
    if project_id:
        # Edit existing project
        existing_project = get_object_or_404(Project, id=project_id)
    else:
        # If there's no project and the user has one assigned, get that project
        existing_project = student.created_project

    # If there's an existing project, allow the user to edit it
    if existing_project:
        if request.method == "POST":
            # Update project with the POST data
            title = request.POST.get("title")
            description = request.POST.get("description")
            skills_input = request.POST.get("skills", "")
            member_limit = int(request.POST.get("member_limit", 4))
            
            # Update project details
            existing_project.title = title
            existing_project.description = description
            existing_project.member_limit = member_limit
            
            # Handle skills input (comma-separated)
            skill_names = [s.strip() for s in skills_input.split(",") if s.strip()]
            existing_project.skills_required.clear()
            for name in skill_names:
                skill, _ = Skill.objects.get_or_create(name=name)
                existing_project.skills_required.add(skill)

            # Save changes to the project
            existing_project.save()

            # Redirect to the project list after saving
            return redirect("projectList")  # Redirect to the project list after saving changes

        # Render the form with pre-filled data from the existing project
        context = {
            "existing_project": existing_project,
        }
        return render(request, "projects/projectProposalPage.html", context)
    
    # If the user doesn't have a project, allow them to create one
    if request.method == "POST":
        # Create a new project if the user doesn't have one yet
        title = request.POST.get("title")
        description = request.POST.get("description")
        skills_input = request.POST.get("skills", "")
        member_limit = int(request.POST.get("member_limit", 4))

        # Create the new project
        project = Project.objects.create(
            title=title,
            description=description,
            member_limit=member_limit,
            status="in_process",
            author=request.user  # Set the user as the author of the project
        )

        # Handle skills input (comma-separated)
        skill_names = [s.strip() for s in skills_input.split(",") if s.strip()]
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name)
            project.skills_required.add(skill)

        project.save()

        # Link the project to the student
        student.created_project = project
        student.save()

        # Redirect to the project list after submission
        return redirect("projectList")

    # If no project exists and it's not a POST request, render the form to create a new one
    return render(request, "projects/projectProposalPage.html")




@login_required(login_url="login")
def studentListPage(request):
    return render(request, "projects/studentListPage.html")
    
@login_required(login_url="login")
def user_logout(request):
    logout(request)  # This logs the user out
    return redirect('login')

@login_required
@require_POST
def toggle_favorite(request, project_id):
    """
    AJAX handler to toggle favorite status for a project.
    """
    project = get_object_or_404(Project, id=project_id)
    user = request.user

    if user in project.favorited_by.all():
        project.favorited_by.remove(user)
        favorited = False
    else:
        project.favorited_by.add(user)
        favorited = True

    return JsonResponse({'favorited': favorited})


def get_user_role(user):
    """Function to return the role of the user"""
    if user.is_superuser:
        return "Admin"
    elif hasattr(user, 'student'):
        return "Student"
    elif hasattr(user, 'advisor'):
        return "Advisor"
    return "UNKNOWN"

def baseView(request):
    return render(request, "base.html")


