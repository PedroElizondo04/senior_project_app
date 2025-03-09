from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
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
def projectProposalPage(request):
    """
    The page to create the project proposal to convince others to join.
    """
    return render(request, "projects/projectProposalPage.html")
