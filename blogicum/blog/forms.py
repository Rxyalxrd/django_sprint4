from django import forms

from .models import Post, User, Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
