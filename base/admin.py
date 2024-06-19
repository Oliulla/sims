from django.contrib import admin

# Register your models here.
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

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(CourseSchedule)
admin.site.register(StudentAdvisor)
admin.site.register(Accommodation)
admin.site.register(Book)
admin.site.register(StudentCourse)
admin.site.register(StudentRegistration)
