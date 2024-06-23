from rest_framework import serializers  # type: ignore
from .models import (
    Student,
    Course,
    CourseSchedule,
    StudentAdvisor,
    Accommodation,
    Book,
    StudentCourse,
    StudentRegistration,
)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            "id",
            "student_number",
            "name",
            "year_of_enrollment",
            "major",
            "gender",
            "email",
            "created_at",
            "updated_at",
        )


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "course_code",
            "course_name",
            "description",
            "credits",
            "created_at",
            "updated_at",
        )


class CourseScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSchedule
        fields = (
            "id",
            "course",
            "semester",
            "year",
            "days_of_week",
            "time",
            "location",
            "created_at",
            "updated_at",
        )


class StudentAdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAdvisor
        fields = (
            "id",
            "student",
            "advisor_name",
            "advisor_email",
            "created_at",
            "updated_at",
        )


class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = (
            "id",
            "student",
            "building_name",
            "room_number",
            "created_at",
            "updated_at",
        )


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "isbn",
            "course",
            "created_at",
            "updated_at",
        )


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = (
            "id",
            "student",
            "course",
            "date_enrolled",
            "created_at",
            "updated_at",
        )


class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRegistration
        fields = (
            "id",
            "student",
            "date_registered",
            "created_at",
            "updated_at",
        )
