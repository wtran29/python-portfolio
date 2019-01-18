from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from apps.blog.models import Blog


blog_detail_url = HyperlinkedIdentityField(
    view_name='blogs-api:detail',
    lookup_field='id',
    lookup_url_kwarg='blog_id'
)


class BlogListSerializer(ModelSerializer):
    url = blog_detail_url
    user = SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "url",
            "user",
            "title",
            "body",
            "pub_date",
        ]

    def get_user(self, obj):
        return str(obj.user.username)


class BlogDetailSerializer(ModelSerializer):
    url = blog_detail_url
    user = SerializerMethodField()
    image = SerializerMethodField()
    html = SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "url",
            "id",
            "user",
            "title",
            "body",
            "html",
            "pub_date",
            "image"
        ]

    def get_html(self, obj):
        return obj.get_html()

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image


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

