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
