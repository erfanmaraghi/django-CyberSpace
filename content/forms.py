from django import forms
from .models import Comment, Post

classes = "form-control rounded-4"


class CommentSendingForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {'content': forms.Textarea(attrs={
            'placeholder': 'Enter your comment',
            'class': classes + " rounded-end-0",
            'rows': '3',
            'style': 'resize:none'
        })}


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'caption', 'content')
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Title of your post',
                'class': classes
            }),
            'content': forms.ClearableFileInput(attrs={
                'class': classes,
                'accept': 'image/*'
            }),
            'caption': forms.Textarea(attrs={
                'placeholder': 'Caption of your post',
                'class': classes,
                'rows': '4',
                'style': 'resize:none'
            })

        }
