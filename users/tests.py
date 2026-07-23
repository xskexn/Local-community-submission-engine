from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import ProjectManager, ProjectMember
from project_management.models import Project 
from submissions.models import Submission 


User = get_user_model()


# View Unit Tests for User Authentication 
class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.manager = ProjectManager.objects.create(
            username="manager1",
            first_name="Jane",
            last_name="Doe",
            email="manager@gmail.com",
            password="password123",
        )
        self.member = ProjectMember.objects.create(
            username="member1",
            first_name="John",
            last_name="Smith",
            email="member@gmail.com",
            password="password123",
            role="VOLUNTEER",
            specialisation="BIODIVERSITY",
        )
        self.admin = ProjectManager.objects.create_superuser(
            username="admin",
            first_name="ad",
            last_name="min",
            email="admin@gmail.com",
            password="password123",
        )

    # login page POST with valid credentials (the project manager is redirected to the full project list)
    def test_user_login_valid_credentials(self):
        response = self.client.post(
            reverse("users:login"),
            {
                "username": "manager1",
                "password": "password123",
            }
        )
        self.assertRedirects(response, reverse("project_management:project_list"))

    # login page POST with invalid credentials (the login page displays an error message)
    def test_user_login_invalid_credentials(self):
        response = self.client.post(
            reverse("users:login"),
            {
                "username": "manager1",
                "password": "wrongpassword",
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertContains(response, "Invalid email or password")

    # logout redirects to home
    def test_user_logout(self):
        self.client.login(username="manager1", password="password123")
        response = self.client.get(reverse("users:logout"))
        self.assertRedirects(response, reverse("home:home"))
        # confirm s that session is cleared
        response = self.client.get(reverse("project_management:project_list"))
        self.assertNotEqual(response.status_code, 200)


# View Unit Tests for Role Assignment
class RoleAssignmentTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@email.com",
            password="password",
        )
        self.member = ProjectMember.objects.create(
            username="member1",
            first_name="John",
            last_name="Smith",
            email="member@email.com",
            password="password123",
            role="VOLUNTEER",
            specialisation="BIODIVERSITY",
        )

    # admin can create a new project member
    def test_admin_can_create_users(self):
        logged_in = self.client.login(username="admin", password="password")
        response = self.client.post(
            reverse("admin:users_projectmember_add"),  
            {
                "username":"testmember",
                "first_name":"test",
                "last_name":"member",
                "email":"testmember@email.com",
                "password":"Strongpassword123!",
                "role":"URBAN_PLANNER", #assigns role at creation
                "specialisation":"ROAD_INFRASTRUCTURE",
                "date_joined_0": "2026-01-01",
                "date_joined_1": "00:00:00",
                "_save": "Save", #save sthe users in the database
            }
        )
        #new_user = User.objects.get(username="testmember")
        #self.member.refresh_from_db()
        #self.assertEqual(new_user.role, "URBAN_PLANNER")
        self.assertTrue(User.objects.filter(username="testmember").exists())
        self.assertEqual(response.status_code, 302)
    
    def test_admin_can_change_role(self):
        self.client.login(username="admin", password="password")
          
        post_data = {
                "username":"testmember",
                "first_name":"test",
                "last_name":"member",
                "email":"testmember@email.com",
                "password":"Strongpassword123!",
                "role":"NGO_COORDINATOR", #change the role
                "specialisation":"ROAD_INFRASTRUCTURE",
                "date_joined_0": "2026-01-01",
                "date_joined_1": "00:00:00",
                "_save": "Save", #save sthe users in the database
            }
        
        response = self.client.post(
        reverse("admin:users_projectmember_change", args=[self.member.pk]),
        post_data
        )
        self.assertEqual(response.status_code, 302)
        self.member.refresh_from_db()
        self.assertEqual(self.member.role, "NGO_COORDINATOR")
        self.assertEqual(response.status_code, 302)


# View Unit Tests for Submission Deletion
class SubmissionDeletionTests(TestCase):
    def setUp(self):
        self.manager = ProjectManager.objects.create(
            username="manager1",
            first_name="Jane",
            last_name="Doe",
            email="manager@email.com",
            password="password123",
        )
        self.member = ProjectMember.objects.create(
            username="member1",
            first_name="John",
            last_name="Smith",
            email="member@email.com",
            password="password123",
            role="VOLUNTEER",
            specialisation="BIODIVERSITY",
        )
        self.project = Project.objects.create(
            name="test project",
            description="test description",
            location_name="test location",
            manager=self.manager,
        )
        self.submission = Submission.objects.create(
            submission_title="test submission",
            submission_category="safety",
            submission_location="test location",
            submission_description="test description",
        )
        

    # project manager can delete a submission
    def test_project_manager_can_delete_submission(self):
        self.client.login(username="manager1", password="password123")
        response = self.client.post(
            reverse("submissions:delete_submission", args=[self.submission.pk])  
        )
        self.assertEqual(Submission.objects.count(), 0)
        self.assertRedirects(response, reverse("submissions:submission_list"))


    # others cannot delete a submission
    def test_others_cannot_delete_submission(self):
        self.client.login(username="member1", password="password123")
        response = self.client.post(
            reverse("submissions:delete_submission", args=[self.submission.pk])  
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Submission.objects.count(), 1)