from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("student/", views.studentApi, name="student"),
    path("student/<int:id>/", views.studentApi, name="student_detail"),
]
