from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ['hash', 'created_by', 'created_at', ]


class ArticleChangeForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ['hash', 'created_by', 'created_at', ]
