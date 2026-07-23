from django import forms
from .models import Project, Task
from users.models import ProjectMember

class ProjectForm(forms.ModelForm):
    # better looking deadline field
    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    # project.manager set in views.py
    # project.team_members can be set in the future
    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "location_name",
            "latitude",
            "longitude",
            "deadline",
            "category",
            
        ]
        #added to make styling simpler in create project html
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
            'location_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter longitude'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select deadline'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

## ADDED TASKS FORM SO THEY CAN EDIT TASKS IN PROJECT SPECIFICS
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["description", "is_complete"]

## added so they can add team members in project specifics
class AddTeamMemberForm(forms.Form):
    team_members = forms.ModelChoiceField(queryset=ProjectMember.objects.all())#only passes in users which arre specifically team members