from django import forms
from project_management.models import Project
from users.models import ProjectManager

class ProjectFilterForm(forms.Form):
    CATEGORY_CHOICES = [('', 'All Categories')] + Project.CATEGORY_CHOICES
    name = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by name...'})
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES, 
        required=False, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    manager = forms.ModelChoiceField(
        queryset=ProjectManager.objects.all(), 
        required=False, 
        empty_label="All Managers",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    deadline_before = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )