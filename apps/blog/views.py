from django.shortcuts import render, HttpResponse, redirect
from .models import Blog
# Create your views here.


def allblogs(request):
    context = {
        'blogs': Blog.objects.order_by('-pub_date').all()
    }
    return render(request, "blog/index.html", context)


def detail(request, blog_id):
    context = {
        'blog': Blog.objects.get(pk=blog_id)
    }
    return render(request, 'blog/blog.html', context)