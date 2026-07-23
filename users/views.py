from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from users.models import ProjectManager, ProjectMember
from project_management.models import Project
from django.contrib import messages


# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if ProjectManager.objects.filter(pk=user.pk).exists() or request.user.is_superuser:
                return redirect("project_management:project_list")
            else:
                return redirect("users:member")
        else:
            return render(request, "login.html", {"error": "Invalid email or password. "})
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("home:home")

def member_view(request):
    projects = Project.objects.filter(team_members=request.user)
    print("Filtered projects:", projects)
    return render(request, "member.html", {'projects': projects})

def csrf_failure(request, reason=""):
    logout(request)
    messages.error(request, "Session expired, please login again.")
    return redirect("users:login")
    #return render(request, 'login.html', {"error": "Session expired. "})