from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, TaskForm, AddTeamMemberForm
from .models import Project, Task
from django.core.exceptions import PermissionDenied
from users.models import ProjectManager
from submissions.models import Submission

# Create your views here.

@login_required
def create_project(request):

#added a check to enure that they are actually a project manager
    if not ( ProjectManager.objects.filter(pk=request.user.pk).exists()) and not request.user.is_superuser:#allows administrators to create
        raise PermissionDenied

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user # set project manager to the current logged in user
            project.save()
            form.save_m2m()
            return redirect("project_management:project_list")
    else: # if GET request -> create empty form
        form = ProjectForm()
    return render(request, "project_management/create_project.html", {"form": form})
    
@login_required
def project_list(request):
    if not ProjectManager.objects.filter(pk=request.user.pk).exists() and not request.user.is_superuser:#allows admins to view projects on main site too
        raise PermissionDenied
    projects = Project.objects.all().order_by("-id")
    submissions = Submission.objects.all()

    return render(
        request,
        "project_management/project_list.html",
        {"projects": projects,
        'submissions': submissions},
    )





#for this I have allowed any user to see project specifics however if they are just a basic user, they will just see project description and other non sensitive things


@login_required


def project_specifics(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()
    team_members = project.team_members.all()
    task_form = TaskForm()
    addTeamMember = AddTeamMemberForm()  

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_task':
            task_form = TaskForm(request.POST)
            if task_form.is_valid():
                task = task_form.save(commit=False)
                task.project = project
                task.save()

        
        elif action == 'complete_task':
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, pk=task_id)
            task.is_complete = 'is_complete' in request.POST
            task.save()

        
        elif action == 'add_team_member':
            user_ids = request.POST.getlist('team_members')
            for user_id in user_ids:
                project.team_members.add(user_id)

    #calculate progress through percentage of tasks completed
    total_tasks = project.tasks.count()
    completed_tasks = project.tasks.filter(is_complete=True).count()
    if completed_tasks != 0:
        progress = int((completed_tasks / total_tasks) * 100)
    else:
        progress = 0

    return render(request, "project_management/project_specifics.html", {
        "project": project,
        "tasks": tasks,
        "team_members": team_members,
        "task_form": task_form,
        "addTeamMember": addTeamMember,
        "progress": progress  
    })