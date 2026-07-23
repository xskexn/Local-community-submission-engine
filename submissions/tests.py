from django.test import TestCase
from django.urls import reverse
from .models import Submission


class SubmissionModelTest(TestCase):
    def setUp(self):
        self.submission = Submission.objects.create(
            submission_title="Broken light",
            submission_category="safety",
            submission_location="Main St",
            submission_description="Street light not working",
        )

    def test_create_submission_success(self):
        """A valid submission is saved to the database."""
        self.client.post(reverse("submissions:create_submission"), {
            "title": "Pothole on Heely Road",
            "category": "infrastructure",
            "location": "1 Heely Street",
            "description": "Large pothole causing hazards.",
        })
        self.assertEqual(Submission.objects.count(), 2)
        new_sub = Submission.objects.latest("pub_date")
        self.assertEqual(new_sub.submission_title, "Pothole on Heely Road")

    def test_create_submission_missing_title(self):
        """A submission without a title is rejected nothing is saved."""
        self.client.post(reverse("submissions:create_submission"), {
            "title": "",
            "category": "safety",
            "location": "2 Heely Road",
            "description": "Missing title test.",
        })
        self.assertEqual(Submission.objects.count(), 1)

    def test_create_submission_missing_description(self):
        """A submission without a description is rejected nothing is saved."""
        self.client.post(reverse("submissions:create_submission"), {
            "title": "Valid Title",
            "category": "general",
            "location": "3 Heely Road",
            "description": "",
        })
        self.assertEqual(Submission.objects.count(), 1)

    def test_create_submission_invalid_category(self):
        """A submission with an invalid category is rejected nothing is saved."""
        self.client.post(reverse("submissions:create_submission"), {
            "title": "Valid Title",
            "category": "aizensosuke",
            "location": "4 Bad Category Lane",
            "description": "Category is not valid.",
        })
        self.assertEqual(Submission.objects.count(), 1)
