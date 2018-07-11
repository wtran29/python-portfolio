from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Work(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    summary = models.TextField()
    video = models.CharField(max_length=5000, blank=True)
    description = models.TextField()
    tech = ArrayField(models.CharField(max_length=1000))
    github = models.CharField(max_length=5000, blank=True)
    deploy = models.CharField(max_length=5000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def bullets(self):
        desc = list(filter(None, self.description.split('.')))
        return desc

