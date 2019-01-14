from urllib.parse import quote_plus
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from .forms import BlogForm
from .models import Blog
# Create your views here.


def allblogs(request):
    blogs_list = Blog.objects.order_by('-updated_at').all()
    paginator = Paginator(blogs_list, 10)  # Show 25 contacts per page
    page_variable = "page"
    page = request.GET.get(page_variable)
    blogs = paginator.get_page(page)
    context = {
        'blogs': blogs
    }
    return render(request, "blog/list.html", context)


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    share_quote = quote_plus(blog.body)
    context = {
        'blog': blog,
        'share_quote': share_quote,

    }
    return render(request, 'blog/detail.html', context)


def create(request):
    form = BlogForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "Successfully created.")
        return redirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, 'blog/form.html', context)


def update(request, blog_id=None):
    instance = get_object_or_404(Blog, pk=blog_id)
    form = BlogForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():

        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "Blog updated.", extra_tags='html_safe')
        return redirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "blog/form.html", context)


def delete(request, blog_id=None):
    instance = get_object_or_404(Blog, pk=blog_id)
    instance.delete()
    messages.success(request, "Successfully deleted.")
    return redirect("blogs:all")
