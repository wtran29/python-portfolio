from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe


from markdown_deux import markdown
from apps.comments.models import Comment

from .utils import get_read_time
# Create your models here.


class BlogManager(models.Manager):
    def active(self, *args, **kwargs):
        # Same as Blog.objects.all() = super(BlogManager, self).all()
        return super(BlogManager, self).filter(draft=False).filter(pub_date__lte=timezone.now())


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    pub_date = models.DateField(auto_now=False, auto_now_add=False)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    video = models.CharField(max_length=5000, blank=True)
    body = models.TextField()
    draft = models.BooleanField(default=False)
    read_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BlogManager()

    def __str__(self):
        return self.title

    def get_html(self):
        content = self.body
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    # def date_only(self):
    #     return self.pub_date.strftime('%e %b %Y')

    def get_absolute_url(self):
        return reverse("blogs:detail", kwargs={"blog_id": self.id})
        # return "/blog/%s" % self.id

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def pre_save_post_receiver(sender, instance, *args, **kwargs):

    if instance.body:
        html_string = instance.get_html()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender=Blog)
