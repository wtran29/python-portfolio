from django.db import models

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='')
    content = models.CharField(max_length=255)
    created_at = models.DateField()
    updated_at = models.DateField()