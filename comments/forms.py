# __author: tzw
# date: 2020/3/18


from django import forms

from comments.models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
