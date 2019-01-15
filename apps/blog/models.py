from django.conf import settings
from django.db import models
from django.urls import reverse
# Create your models here.


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    video = models.CharField(max_length=5000, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:200]+'...'

    # def date_only(self):
    #     return self.pub_date.strftime('%e %b %Y')

    def get_absolute_url(self):
        return reverse("blogs:detail", kwargs={"blog_id": self.id})
        # return "/blog/%s" % self.id
