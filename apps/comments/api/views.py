from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,  # use ?search=, can chain with ?q= search
    OrderingFilter  # shows ordering of search, descending/ascending
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from apps.blog.api.pagination import BlogLimitOffsetPagination, BlogPageNumberPagination
from apps.blog.api.permissions import IsOwnerOrReadOnly

from apps.comments.models import Comment


from .serializers import (
    CommentSerializer,
    CommentDetailSerializer,
)


# class BlogCreateAPIView(CreateAPIView):
#     queryset = Blog.objects.all()
#     serializer_class = BlogCreateUpdateSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = BlogPageNumberPagination  # PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        # blogs_list = super(BlogListAPIView, self).get_queryset(*args, **kwargs)
        comments_list = Comment.objects.all()
        query = self.request.GET.get('q')
        if query:
            comments_list = comments_list.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return comments_list


class CommentDetailAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    lookup_field = "id"
    lookup_url_kwarg = "comment_id"


# class BlogUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = Blog.objects.all()
#     serializer_class = BlogCreateUpdateSerializer
#     lookup_field = "id"
#     lookup_url_kwarg = "blog_id"
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#
#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)


# class BlogDeleteAPIView(DestroyAPIView):
#     queryset = Blog.objects.all()
#     serializer_class = BlogDetailSerializer
#     lookup_field = "id"
#     lookup_url_kwarg = "blog_id"
#     permission_classes = [IsOwnerOrReadOnly]
