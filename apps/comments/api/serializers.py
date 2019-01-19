from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
)

from apps.comments.models import Comment

User = get_user_model()


# Custom CommentCreateSerializer to handle validation for object id and parent
def create_comment_serializer(model_type='blog', slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'updated_at'
            ]

        # Initializing class with the arguments passed
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        # Check to validate content type and if object id is related to it
        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("Not a valid content type")
            # Made to last for other kinds of comments
            # so this serializer can be used in other places
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("Not a slug for this content type")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                primary_user = user
            else:
                primary_user = User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type,
                slug,
                content,
                primary_user,
                parent_obj=parent_obj,
            )
            return comment

    return CommentCreateSerializer


class CommentSerializer(ModelSerializer):
    replies_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "content_type",
            "object_id",
            "parent",
            "content",
            "replies_count",
            "updated_at",
        ]

    def get_replies_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "content",
            "updated_at",
        ]


class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    replies_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "content_type",
            "object_id",
            "content",
            "replies_count",
            "replies",
            "updated_at",
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_replies_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentEditSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "updated_at",
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_replies_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
