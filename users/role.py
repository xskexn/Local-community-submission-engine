from users.models import ProjectManager

def is_manager(request):
    if request.user.is_authenticated:
        is_manager = ProjectManager.objects.filter(pk=request.user.pk).exists()
    else:
        is_manager = False
    return {'is_manager': is_manager}