from django.shortcuts import render, HttpResponse, redirect
from .models import Work
# Create your views here.


def index(request):
    context = {
        'projects': Work.objects
    }
    return render(request, 'work/index.html', context)
