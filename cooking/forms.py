from django import forms
from .models import Post

class PostAddForm(forms.ModelForm):
    """форма для добавления статьи от пользователя"""
    class Meta:
        """"""
        model = Post
        fields = ['title', 'content', 'photo', 'category']
