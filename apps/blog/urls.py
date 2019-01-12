from django.conf.urls import url
from . import views

app_name = 'blogs'
urlpatterns = [
    url(r'^blog$', views.allblogs, name='all'),
    url(r'^blog/(?P<blog_id>\d+)$', views.detail, name='detail'),
    url(r'^blog/update$', views.update),
    url(r'^blog/create$', views.create),
    url(r'^blog/delete$', views.delete)
]