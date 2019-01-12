from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Blog
# Create your views here.


def allblogs(request):
    context = {
        'blogs': Blog.objects.order_by('-pub_date').all()
    }
    return render(request, "blog/index.html", context)


def detail(request, blog_id):
    context = {
        'blog': get_object_or_404(Blog, pk=blog_id)
    }
    return render(request, 'blog/blog.html', context)


def create(request):
    return HttpResponse("<h1>Create</h1>")


def update(request):
    return HttpResponse("<h1>Update</h1>")


def delete(request):
    return HttpResponse("<h1>Delete</h1>")
