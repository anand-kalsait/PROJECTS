from django.http import HttpResponse
from django.shortcuts import render

def about_us(request):
    return HttpResponse("FUCK YOU!")

# Dynamic Url
def courses(request,courseid):
    return HttpResponse(courseid)

def home_page(request):
    return render(request, "index.html")