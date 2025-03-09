from django.urls import path

from . import views
urlpatterns = [
    path("", views.loginPage, name="login"),
    path("landing/<str:role>/", views.landingPage, name="landing"),
    path("projectproposal", views.projectProposalPage, name="projectProposal"),
]
