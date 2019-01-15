from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Blog
from pagedown.widgets import PagedownWidget


class BlogForm(forms.ModelForm):
    body = forms.CharField(widget=PagedownWidget)
    pub_date = forms.DateTimeField(widget=forms.SelectDateWidget)

    class Meta:
        model = Blog

        fields = [
            "title",
            "image",
            "video",
            "body",
            "draft",
            "pub_date",
        ]
        labels = {
            'pub_date': _('Publish Date'),
            'title': _('Blog Title'),
            'video': _('Video Link'),
            'body': _('Content'),
        }

        widgets = {
            "pub_date": forms.DateTimeInput(
                attrs={'class': 'date form-control mb-2', 'id': 'pub_date'}
            ),
            "title": forms.TextInput(
                attrs={'class': 'form-control mb-2'}
            ),
            "image": forms.ClearableFileInput(
                attrs={'class': "form-control mb-2 round"}
            ),
            "video": forms.TextInput(
                attrs={'class': 'form-control mb-2'}
            ),
            "body": forms.Textarea(
                attrs={'class': 'form-control mb-2'}
            ),
        }



