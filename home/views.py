from django.shortcuts import render
from project_management.models import Project
from .forms import ProjectFilterForm

def home(request):
    form = ProjectFilterForm(request.GET)
    project_list = Project.objects.all()
    no_projects_found = False
    if form.is_valid():
        name = form.cleaned_data.get('name')
        category = form.cleaned_data.get('category')
        manager = form.cleaned_data.get('manager')
        deadline_before = form.cleaned_data.get('deadline_before')
        if name:
            project_list = project_list.filter(name__icontains=name)
        if category:
            project_list = project_list.filter(category=category)
        if manager:
            project_list = project_list.filter(manager=manager)
        if deadline_before:
            project_list = project_list.filter(deadline__lte=deadline_before)
        no_projects_found = len(project_list) == 0 and (name or category or manager or deadline_before)

    context = {
        "form": form,
        "projects_list": project_list,
        "no_projects_found": no_projects_found
    }
    return render(request, "home/home.html", context)
