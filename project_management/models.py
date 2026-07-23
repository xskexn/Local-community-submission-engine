
from django.db import models
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User # remove once merged
#from users.models import ProjectManager, ProjectMember -- add once merged
#from submissions.models import Submission -- add once merged


# python manage.py makemigrations
# python manage.py migrate

# to delete all projects:
# python manage.py shell
# from project_management.models import Project
# Project.objects.all().delete()
# exit()

class Project(models.Model):
    #id would be defined here but django does it auto
    
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    location_name = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='managedProjects')
    team_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projectTeams', blank=True)
    #not necessary but I thought would be good for management
    deadline=models.DateTimeField(null=True, blank=True)
    CATEGORY_CHOICES = [
    ('safety', 'Safety'),
    ('accessibility', 'Accessibility'),
    ('greenery', 'Greenery'),
    ('road_maintenance', 'Road Maintenance'),
    ('transport', 'Transport'),
    ('air_quality', 'Air Quality'),
    ('other', 'Other'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)

    #related_submissions = models.ManyToManyField(Submission, blank=True, related_name='linkedprojects')
    #commented out for now as submission model not created 

class Task(models.Model):
    #deletes when project is deleted
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    description = models.CharField(max_length=200)
    is_complete = models.BooleanField(default=False)

