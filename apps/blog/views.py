try:
    from urllib.parse import quote_plus  # Converts string into url format
except:
    pass
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.utils import timezone

from .forms import BlogForm
from .models import Blog
from apps.comments.forms import CommentForm
from apps.comments.models import Comment
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
    # Converting string into url
    share_quote = quote_plus(blog.body)

    initial_data = {
        "content_type": blog.get_content_type,
        "object_id": blog_id
    }
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        print(comment_form.cleaned_data)
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        # Make sure parent obj is there
        parent_obj = None
        # check/parse to see if parent id is there
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        # check if the parent id is in the database,
        # if it exists, we set the parent obj to be the first item in qs
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return redirect(new_comment.content_object.get_absolute_url())

    # This gives all the comments using BlogManager
    comments = blog.comments  # Getting the comments as a property vs qs - Comment.objects.filter_by_instance(blog)
    context = {
        'blog': blog,
        'share_quote': share_quote,
        'comments': comments,
        'comment_form': comment_form,

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
