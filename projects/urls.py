from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path("", views.loginPage, name="home"), 
    path("login/", views.loginPage, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path("landing/", views.landingPage, name="landingPage"),
    path("project/<int:project_id>/view/", views.projectViewPage, name="projectViewPage"),
    path("advisor/", views.advisorListPage, name="advisorList"),
    path("advisor/<int:id>/profile/", views.advisorProfileViewPage, name="advisorProfileView"),
    path("projects/", views.projectListPage, name="projectList"),
    path('projectproposal/', views.projectProposalPage, name='projectProposal'),  # For creating a new project
    path('projectproposal/<int:project_id>/', views.projectProposalPage, name='projectProposal'),  # For editing an existing project
    path("students/", views.studentListPage, name="studentList"),
    path('base/', views.baseView, name='base'),
]

if settings.DEBUG:  # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
