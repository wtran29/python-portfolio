from django.shortcuts import render, HttpResponse, redirect

# Create your views here.


def index(request):
    response = 'Index page for work'
    return HttpResponse(response)
