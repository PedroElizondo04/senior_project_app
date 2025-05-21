from django import forms
from .models import Project, Skill, ProjectApplication
from django_select2.forms import Select2TagWidget


# https://docs.djangoproject.com/en/5.2/topics/forms/
class ProjectForm(forms.ModelForm):
    # https://docs.djangoproject.com/en/5.1/topics/forms/modelforms/#modelform
    class Meta:
        model = Project
        fields = ["title", "description", "skills_required", "member_limit"]
        skills = forms.ModelMultipleChoiceField(
            queryset=Skill.objects.all(),
            widget=forms.SelectMultiple(
                attrs={
                    "class": "select is-multiple has-background-light has-text-black",
                    "style": "background-color: #d3d3d3; border: none; font-weight: bold; max-width: 400px;",
                    "size": "6",  # Controls the visible height of the box
                }
            ),
            required=False,
        )
        # fields = "__all__"
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input is-large has-background-light has-text-black",
                    "placeholder": "Project Title",
                    "style": "background-color: #d3d3d3; border: none; font-weight: bold;",
                    "required": True,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea has-background-light has-text-black",
                    "placeholder": "Description",
                    "style": "background-color: #d3d3d3; border: none; font-weight: bold; min-height: 240px;",
                    "required": True,
                }
            ),
            "member_limit": forms.Select(
                attrs={
                    "class": "select is-custom has-background-light has-text-black",
                    "style": "background-color: #d3d3d3; border: none; font-weight: bold;",
                }
            ),
            "skills_required": forms.SelectMultiple(
                attrs={
                    "class": "select is-multiple has-background-light has-text-black",
                    "style": "background-color: #d3d3d3; border: none; font-weight: bold; max-width: 400px;",
                    "size": "5",  # Number of visible options
                }
            ),
        }


class ApplicationForm(forms.ModelForm):
    # https://docs.djangoproject.com/en/5.1/topics/forms/modelforms/#modelform
    class Meta:
        model = ProjectApplication
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "class": "textarea has-background-light has-text-black",
                    "placeholder": "Why do you want to join this project?",
                    "style": "min-height: 200px; background-color: #d3d3d3; border: none; font-weight: bold;",
                }
            )
        }


# title = forms.CharField(label="Project Title", max_length=40)
# date = forms.DateTimeField(widget=forms.TextInput(attrs={"type": "datetime-local"}))
# description = forms.CharField(widget=forms.Textarea())
# status = forms.ChoiceField(choices=Project.Statuses.choices)
