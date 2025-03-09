from django.urls import path

from . import views
urlpatterns = [
    path("", views.loginPage, name="login"),
    path("landing/<str:role>/", views.landingPage, name="landing"),
    path("<int:project_id>/view/", views.projectViewPage, name="projectViewPage"),
    path("advisor/", views.advisorListPage, name="advisorList"),
    path("projectproposal", views.projectProposalPage, name="projectProposal"),
]
