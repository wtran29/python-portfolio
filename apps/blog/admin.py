from django.contrib import admin

# Register your models here.

from .models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ["__str__", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["title", "body"]

    class Meta:
        model = Blog


admin.site.register(Blog, BlogAdmin)
