from django.shortcuts import render
from project_management.models import Project
import json

def map(request):
    project_list = list(Project.objects.values('name', 'latitude', 'longitude'))
    context = {
        'projects_list': project_list
    }
    print(project_list)
    return render(request, 'map.html', context)