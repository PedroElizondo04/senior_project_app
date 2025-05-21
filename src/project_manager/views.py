from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, IntegerField, Value, When
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views import View, generic

from .forms import ApplicationForm, ProjectForm
from .models import Project, ProjectApplication, AdvisorProfile, User
from django.contrib.auth import get_user_model

User = get_user_model()
# We're using class-based views.
# https://docs.djangoproject.com/en/5.1/topics/class-based-views/generic-display/


class LandingPage(LoginRequiredMixin, generic.TemplateView):
    login_url = "accounts/login"
    template_name = "project_manager/landingPage.html"


class ProjectListPage(LoginRequiredMixin, generic.ListView):
    login_url = "accounts/login"
    template_name = "project_manager/projectListPage.html"
    context_object_name = "pending_projects_list"

    def get_queryset(self):
        """Return the list of pubdate"""
        return (
            Project.objects.filter(status="pending")
            .annotate(
                # Order by user creations first:
                is_mine=Case(
                    When(created_by=self.request.user, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            )
            .order_by("is_mine", "-created_date")
        )


class ProjectDetailPage(LoginRequiredMixin, generic.DetailView):
    login_url = "accounts/login"
    model = Project
    template_name = "project_manager/projectDetailPage.html"


class ProjectEditPage(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "project_manager/projectEditPage.html"

    def get_success_url(self):
        return reverse("manager:projectDetail", args=[self.object.id])


class ProjectProposalPage(LoginRequiredMixin, View):
    login_url = "accounts/login"
    form_class = ProjectForm
    template_name = "project_manager/projectProposalPage.html"

    # GET form template :^D
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    # POST form to db :^D
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project = form.save()
            return redirect(reverse("manager:projectDetail", args=[project.id]))
        return render(request, self.template_name, {"form": form})


class ProjectDeleteView(generic.DeleteView):
    model = Project
    template_name = "project_manager/project_confirm_delete.html"
    success_url = reverse_lazy("manager:projectList")


class ProjectApplicationPage(LoginRequiredMixin, generic.FormView):
    form_class = ApplicationForm
    template_name = "project_manager/projectApplicationPage.html"

    def get_project(self):
        return get_object_or_404(Project, pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        project = self.get_project()
        form = self.get_form()
        return self.render_to_response(
            self.get_context_data(form=form, project=project)
        )

    def form_valid(self, form):
        project = self.get_project()
        applicant = self.request.user
        message = form.cleaned_data["message"]

        # Create the application
        application = ProjectApplication.objects.create(
            project=project, applicant=applicant, message=message
        )

        # Redirect to the project detail page aftera the user applies
        return HttpResponseRedirect(reverse("manager:projectDetail", args=[project.id]))

    def form_invalid(self, form):
        project = self.get_project()
        return self.render_to_response(
            self.get_context_data(form=form, project=project)
        )


class AdvisorListPage(LoginRequiredMixin, generic.ListView):
    login_url = "accounts/login"
    template_name = "project_manager/advisorListPage.html"
    context_object_name = "advisors_list"

    def get_queryset(self):
        """Return the list of pubdate"""
        return User.objects.filter(user_type=User.UserTypes.ADVISOR).select_related(
            "advisorprofile"
        )


class AdvisorDetailPage(generic.DetailView):
    model = AdvisorProfile
    template_name = "project_manager/advisorDetailPage.html"
    context_object_name = "advisor"


class ProjectApplicationListView(LoginRequiredMixin, generic.ListView):
    model = ProjectApplication
    template_name = "project_manager/projectApplicationList.html"
    context_object_name = "applications"

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["pk"])
        if project.created_by != self.request.user:
            raise PermissionDenied
        return ProjectApplication.objects.filter(project=project)


class ProjectApplicationDetailView(LoginRequiredMixin, generic.DetailView):
    model = ProjectApplication
    template_name = "project_manager/projectApplicationDetailView.html"
    context_object_name = "application"

    def get_object(self):
        application = super().get_object()
        if application.project.created_by != self.request.user:
            raise PermissionDenied("You are not allowed to view this application.")
        return application

    def post(self, request, *args, **kwargs):
        application = self.get_object()

        if "admit" in request.POST:
            project = application.project
            if project.members.count() < project.member_limit:
                project.members.add(application.applicant)
                application.delete()
            else:
                return redirect("manager:projectDetail", pk=project.pk)

        elif "discard" in request.POST:
            application.delete()
        return redirect("manager:projectDetail", pk=application.project.pk)
