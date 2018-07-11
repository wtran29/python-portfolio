from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^blog$', views.allblogs, name='blogs'),
    url(r'^blog/(?P<blog_id>\d+)$', views.detail)
]