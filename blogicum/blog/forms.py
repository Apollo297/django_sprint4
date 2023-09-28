from django import forms 
from django.contrib.auth import get_user_model

from .models import Post, Comment


User = get_user_model()


class PostForm(forms.ModelForm):

    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)


# class PasswordForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = ('password',)
