from django.conf.urls import url
from . import views

app_name = 'blogs'
urlpatterns = [
    url(r'^$', views.allblogs, name='all'),
    url(r'^(?P<blog_id>\d+)$', views.detail, name='detail'),
    url(r'^(?P<blog_id>\d+)/edit$', views.update, name='update'),
    url(r'^create$', views.create),
    url(r'^(?P<blog_id>\d+)/delete$', views.delete, name='delete')
]