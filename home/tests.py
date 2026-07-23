from django.test import TestCase
from django.urls import reverse
from project_management.models import Project

# Create your tests here.
class HomePageTest(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(
            name="Test Project 1", 
            category="Safety", 
            latitude=52.45, 
            longitude=-1.93,
        )
        self.project2 = Project.objects.create(
            name="Test Project 2", 
            category="Accessibility", 
            latitude=52.45, 
            longitude=-1.83,
        )
        self.url = reverse("home:home")
    def test_projects_in_context(self):
        """projects_list must be in the template context."""
        response = self.client.get(self.url)
        self.assertIn('projects_list', response.context)
    def test_filter_dashboard_by_name(self):
        """Filter dashboard should corretly filter projects by name."""
        response = self.client.get(self.url, {'name': 'Test Project 1'})
        self.assertEqual(len(response.context['projects_list']), 1)
        self.assertEqual(response.context['projects_list'][0].name, "Test Project 1")
        self.assertFalse(response.context['no_projects_found'])
    def test_filter_dashboard_no_results(self):
        """no_projects_found must be true if the filter dashboard finds no projects."""
        response = self.client.get(self.url, {'name': 'dwasdfawdjnk'})
        self.assertEqual(len(response.context['projects_list']), 0)
        self.assertTrue(response.context['no_projects_found'])
    def test_high_contrast_button_in_template(self):
        """The high-contrast toggle must be in the home template"""
        response = self.client.get(self.url)
        self.assertContains(response, 'id="highContrastToggle"')
        self.assertContains(response, 'Toggle high contrast mode')
        self.assertContains(response, "localStorage.getItem('highContrast') === 'enabled'")
        self.assertContains(response, "htmlElement.classList.toggle('high-contrast');")
    def test_interactive_map_in_template(self):
        """The interactive map must be in the template"""
        response = self.client.get(self.url)
        self.assertContains(response, 'leaflet.css')
        self.assertContains(response, 'leaflet.js')
        self.assertContains(response, 'id="map"')
        expected_marker = f"L.marker([{self.project1.latitude}, {self.project1.longitude}]"
        self.assertContains(response, expected_marker)
        self.assertContains(response, self.project1.name)
        self.assertContains(response, self.project1.description)