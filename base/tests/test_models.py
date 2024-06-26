import unittest
from django.test import TestCase
from base.models import Student


class StudentTestCase(TestCase):

    def setUp(self):
        # Setup any necessary data or state before each test
        Student.objects.create(name="Alice", age=20, major="Computer Science")
        Student.objects.create(name="Bob", age=22, major="Engineering")

    def test_student_creation(self):
        """Test creating a student instance."""
        alice = Student.objects.get(name="Alice")
        bob = Student.objects.get(name="Bob")

        self.assertEqual(alice.major, "Computer Science")
        self.assertEqual(bob.age, 22)

    def test_student_deletion(self):
        """Test deleting a student instance."""
        alice = Student.objects.get(name="Alice")
        alice.delete()

        # Verify Alice is no longer in the database
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(name="Alice")


if __name__ == "__main__":
    unittest.main()
