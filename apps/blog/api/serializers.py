from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

from apps.blog.models import Blog


blog_detail_url = HyperlinkedIdentityField(
    view_name='blogs-api:detail',
    lookup_field='id',
    lookup_url_kwarg='blog_id'
)


class BlogListSerializer(ModelSerializer):
    url = blog_detail_url

    class Meta:
        model = Blog
        fields = [
            "url",
            "id",
            "user",
            "title",
            "body",
            "pub_date",
        ]


class BlogDetailSerializer(ModelSerializer):
    url = blog_detail_url

    class Meta:
        model = Blog
        fields = [
            "url",
            "id",
            "title",
            "body",
            "pub_date",
        ]


class BlogCreateUpdateSerializer(ModelSerializer):
    url = blog_detail_url

    class Meta:
        model = Blog
        fields = [
            "url",
            "title",
            "body",
            "pub_date",
        ]

