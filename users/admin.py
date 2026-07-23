from django.contrib import admin
from users.models import CustomUser, ProjectManager, ProjectMember

# Register your models here.

#registering just makes sure all these models show up in the admin panel -> /website/admin/
#admin.site.register(CustomUser)
admin.site.register(ProjectManager)
admin.site.register(ProjectMember)