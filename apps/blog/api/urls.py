from django.conf.urls import url
from apps.blog.api.views import (
    BlogListAPIView,
    BlogDetailAPIView,
    BlogUpdateAPIView,
    BlogDeleteAPIView
)

app_name = 'blogs'
urlpatterns = [
    url(r'^$', BlogListAPIView.as_view(), name='all'),
    url(r'^(?P<blog_id>\d+)$', BlogDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<blog_id>\d+)/edit$', BlogUpdateAPIView.as_view(), name='update'),
    # url(r'^create$', views.create),
    url(r'^(?P<blog_id>\d+)/delete$', BlogDeleteAPIView.as_view(), name='delete')
]