from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Blog
from pagedown.widgets import PagedownWidget
# from crispy_forms.helper import FormHelper


class BlogForm(forms.ModelForm):
    body = forms.CharField(widget=PagedownWidget(show_preview=False), label='Content')
    pub_date = forms.DateField(widget=forms.SelectDateWidget, label='Publish Date')

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
            'pub_date': 'Publish Date',
            'title': 'Blog Title',
            'video': 'Video Link',
            'body': 'Content',
        }

        widgets = {
            "image": forms.ClearableFileInput(
                attrs={'class': "form-control mb-2 round"}
            ),
            # "body": forms.CharField(
            #     widget=PagedownWidget(
            #         show_preview=False),
            # ),
            # "pub_date": forms.DateField(
            #     widget=forms.SelectDateWidget
            # ),
        }

    # helper = FormHelper()
    # helper.form_method = 'POST'
    # helper.add_input(('Submit', 'Submit', css_class='btn-primary'))


