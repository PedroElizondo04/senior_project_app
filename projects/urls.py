from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path("", views.loginPage, name="login"),
    path("landing/<str:role>/", views.landingPage, name="landing"),
    path("<int:project_id>/view/", views.projectViewPage, name="projectViewPage"),
    path("advisor/", views.advisorListPage, name="advisorList"),
    path("advisor/<str:name>", views.advisorProfileViewPage, name="advisorProfileView"),
    path("projects/", views.projectListPage, name="projectList"),
    path("projectproposal", views.projectProposalPage, name="projectProposal"),
]

if settings.DEBUG:  # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)