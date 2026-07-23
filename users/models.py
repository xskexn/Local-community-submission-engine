from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser): #tells Django to use this model instead of the default one
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)


    REQUIRED_FIELDS = ['first_name','last_name', 'email']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):# hashes the password if a user is created through the admin site, so django can authenticate
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Customer"

    #this is a parent class both Project Manager and Project Member inherit from, not a real user, just used to hold the
    #shared attributes of both of them (since there are quite a few)

class ProjectManager(CustomUser):
    is_staff = True #gives access to admin panel
    #makes it show up as Project manegr in admin panel not just user
    class Meta:
        verbose_name = "Project Manager"


    #attributes: first name, last name, email ,username, password, is_staff (True by default), date_joined, last_login

class ProjectMember(CustomUser):
    organisation = models.CharField(max_length=100, blank=True, default = "Independent")

    ROLE_CHOICES = [('VOLUNTEER', 'Volunteer'), ('URBAN_PLANNER', 'Urban Planner'), ('NGO_COORDINATOR', 'NGO Coordinator'), ('LOCAL_RESIDENT_REP', 'Local Resident Rep') ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    SPECIALISATION_CHOICES = [("WASTE_MANAGEMENT","Waste Management"),("BIODIVERSITY","Biodiversity"),("ROAD_INFRASTRUCTURE","Road Infrastructure"),("VEGETATION","Vegetation") ]
    specialisation = models.CharField(max_length=50, choices=SPECIALISATION_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_specialisation_display()}"
    

    class Meta:
        verbose_name = "Project Member"

    #attributes: first name, last name, email , username, password, organisation (independent by default), 
    # role (basically their job title), specialisation (to help managers decide who to assign), date_joined last_login


