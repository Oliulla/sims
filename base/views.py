from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser  # type: ignore
from django.http import JsonResponse
from .models import Student
from .serializers import StudentSerializer

from django.shortcuts import render
from .data_analysis import perform_analysis


def home(request):
    analysis_results = perform_analysis()
    context = {"analysis_results": analysis_results}
    return render(request, "base/home.html", context)


@csrf_exempt
def studentApi(request, id=0):
    if request.method == "GET":
        if id != 0:
            student = get_object_or_404(Student, pk=id)
            student_serializer = StudentSerializer(student)
            return JsonResponse(student_serializer.data, safe=False)
        else:
            students = Student.objects.all()
            students_serializer = StudentSerializer(students, many=True)
            return JsonResponse(students_serializer.data, safe=False)

    elif request.method == "POST":
        student_data = JSONParser().parse(request)
        student_serializer = StudentSerializer(data=student_data)
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse(
                {
                    "status": 201,
                    "message": "Request Success",
                    "data": student_serializer.data,
                },
                status=201,
            )
        return JsonResponse(student_serializer.errors, status=400)

    elif request.method == "PATCH":
        student_data = JSONParser().parse(request)
        student = get_object_or_404(Student, id=student_data["id"])
        student_serializer = StudentSerializer(student, data=student_data)
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed To update", safe=False)

    elif request.method == "DELETE":
        student = get_object_or_404(Student, id=id)
        student.delete()
        return JsonResponse("Deleted successfully", safe=False)
