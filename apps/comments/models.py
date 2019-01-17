from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.urls import reverse
# Create your models here.


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        # Getting the content type from Blog model
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id  # Same as Blog.objects.get(id=blog.id)
        # This gives all the comments related to the blog
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        return qs


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse("comments:thread", kwargs={'comment_id': self.id})

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"comment_id": self.id})

    def children(self):  # Replies to comments
        return Comment.objects.filter(parent=self).order_by("created_at")

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
