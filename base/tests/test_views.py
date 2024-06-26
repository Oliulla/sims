from django.test import TestCase, Client
from django.urls import reverse
from base.models import Student  # Import your models as needed


class TestStudentViews(TestCase):

    def setUp(self):
        # Set up any necessary data or configurations before each test
        self.client = Client()
        self.student = Student.objects.create(
            first_name="John",
            last_name="Doe",
            age=20,
            major="Computer Science",
            gender="Male",
            region="North",
            year_of_enrollment=2020,
        )
        # Add more setup as needed for your specific views

    def test_student_list_view(self):
        # Test student list view
        url = reverse("student-list")  # Replace with your URL name if different
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "base/student_list.html"
        )  # Ensure correct template used
        self.assertContains(
            response, self.student.first_name
        )  # Check if student data appears

    def test_student_detail_view(self):
        # Test student detail view
        url = reverse("student-detail", kwargs={"pk": self.student.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "base/student_detail.html"
        )  # Ensure correct template used
        self.assertContains(
            response, self.student.first_name
        )  # Check if student data appears

    # Add more tests for other views as needed

    # Example of a post request test
    def test_post_request(self):
        # Test a POST request to create a new student
        url = reverse("student-create")  # Replace with your URL name if different
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "age": 21,
            "major": "Biology",
            "gender": "Female",
            "region": "South",
            "year_of_enrollment": 2021,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, 302
        )  # Check for successful redirect or other status code
