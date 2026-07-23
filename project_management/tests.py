from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Project, Task

# python manage.py test project_management

# Create your tests here.

User = get_user_model()

# Model Unit Tests for F1 ⟶ Creation of a project
class ProjectModelTests(TestCase):
    # create a project directly in the database with all valid fields
    def test_create_project_with_valid_fields(self):
        user = User.objects.create_user(username="user1",password="password")
        project = Project.objects.create(
            name="test name",
            description="test description",
            location_name="test location",
            manager=user,
        )
        self.assertEqual(project.name, "test name")
        self.assertEqual(project.description, "test description")
        self.assertEqual(project.location_name, "test location")
        self.assertEqual(project.manager, user)

    # create a project where the description is blank
    def test_create_project_with_blank_description(self):
        user = User.objects.create_user(username="user2", password="password")
        project = Project.objects.create(
            name="test name",
            description="",
            location_name="test location",
            manager=user,
        )
        self.assertEqual(project.description, "")

# View Unit Tests for F1 ⟶ Creation of a project
class ProjectViewTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@email.com",
            password="password"
        )
        self.normal_user = User.objects.create_user(
            username="user",
            password="password"
        )
        
    # create_project page GET
    def test_create_project_loads(self):
        self.client.login(username="admin",password="password")
        response = self.client.get(reverse("project_management:create_project"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project_management/create_project.html")
        self.assertContains(response, "form")

    # create valid project POST 
    def test_valid_post_request_creates_project(self):
        self.client.login(username="admin",password="password")
        response= self.client.post(
            reverse("project_management:create_project"),
            {
                "name": "test name",
                "description": "test description",
                "location_name": "test location",
                "category": "safety",
            }
        )
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.name, "test name")
        self.assertEqual(project.manager, self.admin)
        self.assertRedirects(response, reverse("project_management:project_list"))

    # create invalid project POST
    def test_invalid_post_request_creates_project(self):
        self.client.login(username="admin",password="password")
        response=self.client.post(
            reverse("project_management:create_project"),
            {
                "name":"",
                "description": "test description",
                "location_name": "test location",
            }
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(Project.objects.count(), 0)

    # test that normal users can't create projects
    def test_unauthorised_user_denied_from_project(self):
        self.client.login(username="user",password="password")
        response=self.client.get(reverse("project_management:create_project"))
        self.assertEqual(response.status_code, 403)

# Model Unit Tests for F2 ⟶ Adding tasks to a project.
class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user",password="password")
        self.project = Project.objects.create(
            name="test project",
            description="test description",
            location_name="test location",
            manager=self.user,
        )

    # create a task with all valid fields
    def test_create_task(self):
        task = Task.objects.create(
            project=self.project,
            description="test description",
        )
        self.assertEqual(task.project,self.project)
        self.assertEqual(task.description,"test description")

# View Unit Tests for F2 ⟶ Adding tasks to a project.
class TaskViewTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@email.com",
            password="password"
        )
        self.project = Project.objects.create(
            name="test name",
            description="test description",
            location_name="test location",
            manager=self.admin
        )
    
    # project_specifics page GET
    def test_project_specifics_loads(self):
        self.client.login(username="admin", password="password")
        response=self.client.get(
            reverse("project_management:project_specifics", args=[self.project.pk])
        )
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, "project_management/project_specifics.html")
        self.assertEqual(response.context["project"], self.project)

    # add valid task POST
    def test_add_valid_task(self):
        self.client.login(username="admin",password="password")
        response=self.client.post(
            reverse("project_management:project_specifics", args=[self.project.pk]),
            {
                "action": "add_task",
                "description": "test description",
            }
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.project, self.project)
        self.assertEqual(task.description, "test description")
        self.assertFalse(task.is_complete)

    # add invalid task POST
    def test_add_invalid_task(self):
        self.client.login(username="admin",password="password")
        response=self.client.post(
            reverse("project_management:project_specifics",args=[self.project.pk]),
            {
                "action": "add_task",
                "description": "",
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)

# Unit Tests for F3 ⟶ Assigning users to a project
class ProjectUserTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@email.com",
            password="password"
        )
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@email.com",
            password="password"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@email.com",
            password="password"
        )
        self.project=Project.objects.create(
            name="test name",
            description="test description",
            location_name="test location",
            manager=self.admin
        )

    # add user to project    
    def test_add_user_to_project(self):
        self.client.login(username="admin",password="password")
        response=self.client.post(
            reverse("project_management:project_specifics", args=[self.project.pk]),
            {
                "action": "add_team_member",
                "team_members": [self.user1.pk],
            }
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.project.team_members.count(), 1)
        self.assertIn(self.user1,self.project.team_members.all())

    # add users to project
    def test_add_users_to_project(self):
        self.client.login(username="admin",password="password")
        response=self.client.post(
            reverse("project_management:project_specifics", args=[self.project.pk]),
            {
                "action": "add_team_member",
                "team_members": [self.user1.pk,self.user2.pk],
            }
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.project.team_members.count(), 2)
        self.assertIn(self.user1,self.project.team_members.all())
        self.assertIn(self.user2,self.project.team_members.all())

# Integration Tests for F3
class ProjectUserIntegrationTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@email.com",
            password="password"
        )
        self.normal_user = User.objects.create_user(
            username="user",
            email="user@email.com",
            password="password"
        )

    # login -> view project -> add user -> view project
    def test_add_user_then_view_project(self):
        self.client.login(username="admin",password="password")
        # create project
        create_response = self.client.post(
            reverse("project_management:create_project"),
            {
                "name":"test name",
                "description":"test description",
                "location_name": "test location",
                "category": "other",
            }
        )
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.manager,self.admin)
        # view project specifics
        response = self.client.get(
            reverse("project_management:project_specifics", args=[project.pk])
        )
        self.assertEqual(response.status_code,200)
        # add user
        response=self.client.post(
            reverse("project_management:project_specifics", args=[project.pk]),
            {
                "action": "add_team_member",
                "team_members": [self.normal_user.pk],
            },
            follow =True
        )
        self.assertEqual(response.status_code,200)

        project.refresh_from_db()

        self.assertEqual(project.team_members.count(), 1)
        self.assertIn(self.normal_user, project.team_members.all())
        # view project specifics
        response = self.client.get(
            reverse("project_management:project_specifics", args = [project.pk])
        )
        self.assertEqual(response.status_code,200)
        self.assertContains(response, self.normal_user.username)

# Integration Tests for F1, F2
class IntegrationTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@email.com",
            password="password"
        )
        self.normal_user = User.objects.create_user(
            username="user",
            password="password"
        )
    
    def test_authorised_user_can_create_project(self):
        self.client.login(username="admin",password="password")
        response=self.client.post(
            reverse("project_management:create_project"),
            {
                "name": "test name",
                "description": "test description",
                "location_name": "test location",
                "category": "other",
            },
            follow=True
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.name, "test name")
        self.assertEqual(project.manager, self.admin)

    def test_invalid_submission_doesnt_create_project(self):
        self.client.login(username="admin",password="password")
        response=self.client.post(
            reverse("project_management:create_project"),
            {
                "name": "",
                "description": "test description",
                "location_name": "test location",
            }
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(Project.objects.count(),0)
    
    def test_create_project_then_add_task(self):
        self.client.login(username="admin",password="password")
        create_response = self.client.post(
            reverse("project_management:create_project"),
            {
                "name": "test name",
                "description": "test description",
                "location_name": "test location",
                "category": "other",
            }
        )
        self.assertEqual(Project.objects.count(), 1)
        project=Project.objects.first()
        task_response=self.client.post(
            reverse("project_management:project_specifics", args=[project.pk]),
            {
                "action": "add_task",
                "description": "test description",
            },
            follow = True
        )
        self.assertEqual(task_response.status_code,200)
        self.assertEqual(Task.objects.count(),1)
        task = Task.objects.first()
        self.assertEqual(task.project, project)
        self.assertEqual(task.description,"test description")

    def test_project_specifics_displays_completed_task(self):
        self.client.login(username="admin",password="password")
        project=Project.objects.create(
            name="test name",
            description="test description",
            location_name="test location",
            manager=self.admin
        )
        task = Task.objects.create(
            project=project,
            description="test description",
            is_complete = False
        )
        self.client.post(
            reverse("project_management:project_specifics", args=[project.pk]),
            {
                "action": "complete_task",
                "task_id": task.id,
                "is_complete": "on"
            }
        )
        task.refresh_from_db()
        self.assertTrue(task.is_complete)
        response=self.client.get(
            reverse("project_management:project_specifics", args=[project.pk])
        )
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "test description")

    def test_invalid_task_submission_does_not_create_task(self):
        self.client.login(username="admin",password="password")

        project = Project.objects.create(
            name="test name",
            description="test description",
            location_name="test location",
            manager=self.admin,
        )
        response=self.client.post(
            reverse("project_management:project_specifics",args=[project.pk]),
            {
                "action": "add_task",
                "description": "",
            }
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(project.tasks.count(), 0)