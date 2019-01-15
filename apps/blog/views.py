from urllib.parse import quote_plus
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, Http404
from django.contrib import messages
from .forms import BlogForm
from .models import Blog
# Create your views here.


def allblogs(request):
    today = timezone.now().date()
    blogs_list = Blog.objects.active().order_by('-pub_date')
    if request.user.is_staff or request.user.is_superuser:
        blogs_list = Blog.objects.all().order_by('-pub_date')

    query = request.GET.get('q')
    if query:
        blogs_list = blogs_list.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(blogs_list, 2)  # Show 25 contacts per page
    page_variable = "page"
    page = request.GET.get(page_variable)
    blogs = paginator.get_page(page)
    context = {
        'blogs': blogs,
        'today': today,
        'page_variable': page_variable
    }
    return render(request, "blog/list.html", context)


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if blog.draft or blog.pub_date > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_quote = quote_plus(blog.body)
    context = {
        'blog': blog,
        'share_quote': share_quote,

    }
    return render(request, 'blog/detail.html', context)


def create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated:
        raise Http404

    form = BlogForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully created.")
        return redirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, 'blog/form.html', context)


def update(request, blog_id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Blog, pk=blog_id)
    instance.delete()
    messages.success(request, "Successfully deleted.")
    return redirect("blogs:all")
