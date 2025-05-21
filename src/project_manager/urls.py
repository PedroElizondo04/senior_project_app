from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "manager"
urlpatterns = [
    path(
        "",
        views.LandingPage.as_view(),
        name="landingPage",
    ),
    path(
        "projects/",
        views.ProjectListPage.as_view(),
        name="projectList",
    ),
    path(
        "project/<int:pk>/",
        views.ProjectDetailPage.as_view(),
        name="projectDetail",
    ),
    path("propose/", views.ProjectProposalPage.as_view(), name="projectProposal"),
    path(
        "project/<int:pk>/apply/",
        views.ProjectApplicationPage.as_view(),
        name="projectApplication",
    ),
    path(
        "project/<int:pk>/edit/",
        views.ProjectEditPage.as_view(),
        name="projectEdit",
    ),
    path(
        "project/<int:pk>/delete/",
        views.ProjectDeleteView.as_view(),
        name="projectDelete",
    ),
    path(
        "advisors/",
        views.AdvisorListPage.as_view(),
        name="advisorList",
    ),
    path("advisors/<int:pk>/", views.AdvisorDetailPage.as_view(), name="advisorDetail"),
    path(
        "project/<int:pk>/applications/",
        views.ProjectApplicationListView.as_view(),
        name="projectApplications",
    ),
    path(
        "application/<int:pk>/",
        views.ProjectApplicationDetailView.as_view(),
        name="applicationDetail",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
