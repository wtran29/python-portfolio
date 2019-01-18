from rest_framework.serializers import ModelSerializer

from apps.blog.models import Blog


class BlogListSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "user",
            "title",
            "body",
            "pub_date",
        ]


class BlogDetailSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "body",
            "pub_date",
        ]


class BlogCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "title",
            "body",
            "pub_date",
        ]