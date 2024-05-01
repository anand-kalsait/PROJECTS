from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    data = {
        "title":"Home_Page",
        "bdata":"Welcome to the Django Project......",
        "names":["Anand","Pratik","Prashant","Shruti","Sharad"],
        "details":[
            {"name":"Anand", "education":"CS Engineering"},
            {"name":"Pratik", "education":"Civil Engineering"},
            {"name":"Prashant", "education":"12th"},
            {"name":"Shruti", "education":"10th"},
            {"name":"Sharad", "education":"9th"}
        ],
        "numbers":[j for j in range(1,101)]

    }
    return render(request, "index.html",data)

def about_us(request):
    return HttpResponse("FUCK YOU!")

# Dynamic Url
def courses(request,courseid):
    return HttpResponse(courseid)

