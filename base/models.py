from django.db import models


# Gender Choices
class GenderChoices(models.TextChoices):
    MALE = "Male", "Male"
    FEMALE = "Female", "Female"
    OTHER = "Other", "Other"


# Base model with timestamp fields
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Student model
class Student(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    student_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    year_of_enrollment = models.IntegerField()
    major = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.student_number})"


# Course model
class Course(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.IntegerField()

    def __str__(self):
        return self.course_name


# CourseSchedule model
class CourseSchedule(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10)
    year = models.IntegerField()
    days_of_week = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.course.course_name} - {self.semester} {self.year}"


# StudentAdvisor model
class StudentAdvisor(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    advisor_name = models.CharField(max_length=150)
    advisor_email = models.EmailField()

    def __str__(self):
        return f"{self.student.name} - {self.advisor_name}"


# Accommodation model
class Accommodation(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    building_name = models.CharField(max_length=150)
    room_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.student.name} - {self.building_name} {self.room_number}"


# Book model
class Book(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# StudentCourse model (to handle many-to-many relationship between Student and Course)
class StudentCourse(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name}"


# StudentRegistration model (for registering/updating student information)
class StudentRegistration(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_registered = models.DateField()

    def __str__(self):
        return f"{self.student.name} - Registered on {self.date_registered}"
