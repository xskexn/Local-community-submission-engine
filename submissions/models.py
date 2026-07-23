from django.db import models

# Create your models here.
class Submission(models.Model):
    submission_title = models.CharField(max_length=200, blank=False)
    submission_category = models.CharField(blank=False, max_length=50, choices=[
        ("general", "General"),
        ("safety", "Safety"),
        ("infrastructure", "Infrastructure"),
        ("event", "Event"),
    ])
    submission_location = models.CharField(max_length=255, blank=False)
    submission_description = models.TextField(blank=False)
    #submission_photo = models.ImageField(upload_to="photos/", blank=True, null=True) working simple for now as the photo is optional 
    pub_date = models.DateTimeField(auto_now_add=True)