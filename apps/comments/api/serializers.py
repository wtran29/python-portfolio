from django.contrib.contenttypes.models import ContentType

from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
)

from apps.comments.models import Comment


# Custom CommentCreateSerializer to handle validation for object id and parent
def create_comment_serializer(model_type='POST', object_id=None, parent_id=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'parent',
                'content',
                'updated_at'
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.object_id = object_id
            self.parent_obj = None
            if self.parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("Not a valid content type")
            # Made to last for other kinds of comments
            # so this serializer can be used in other places
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(object_id=self.object_id)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("Not an object id for this content type")
            return data

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
