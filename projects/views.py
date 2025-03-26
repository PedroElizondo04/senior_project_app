from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.shortcuts import redirect
from .models import Project, Skill
# Create your views here.

# def loginPage(request):
#     return HttpResponse("Welcome Faculty and Students! Login to access your senior project!")
#
# def landingPage(request, role):
#     context = { "role": role.upper(), }
#     return render(request,"projects/landingPage.html", context)
#
#
#
# def projectViewPage(request, project_id):
#     return HttpResponse(f"You're looking at project_id {project_id}")
#

def loginPage(request):
    """
    The login page for all users.
    """
    return render(request, "projects/loginPage.html")
def landingPage(request, role):
    """
    The landing page for all users. Contains big action buttons depending on the role.
    """
    context = { "role": role.upper(), }
    return render(request, "projects/landingPage.html", context)
def projectViewPage(request, project_id):
    """
    The view page of a project to see its author, description, skills, etc.
    """
    context = { "project_id": project_id, }
    return render(request, "projects/projectViewPage.html", context)
def advisorListPage(request):
    """
    View a list of advisors and their contact information. 
    """
    return render(request, "projects/advisorListPage.html")
def advisorProfileViewPage(request, name):
    """
    View an individual advisor and their contact information.
    """
    context = { "name": name, }
    return render(request, "projects/advisorProfileViewPage.html", context)
def projectListPage(request):
    """
    The list page for projects, contains a table of projects and the ability to filter, apply, etc.
    """
    projects = Project.objects.all()
    return render(request, "projects/projectListPage.html", {'projects': projects})
def projectProposalPage(request):
    """
    The page to create the project proposal to convince others to join.
    """
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        skills_input = request.POST.get("skills", "")
        member_limit = int(request.POST.get("member_limit", 4))

        # Create the project
        project = Project.objects.create(
            title=title,
            description=description,
            member_limit=member_limit,
            status="in_process",
        )

        # Handle skills input (comma-separated)
        skill_names = [s.strip() for s in skills_input.split(",") if s.strip()]
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name)
            project.skills_required.add(skill)

        project.save()
        return redirect("projectList") # Go back to the tihngy

    return render(request, "projects/projectProposalPage.html")
