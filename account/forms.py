from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

classes = "form-control rounded-4"


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Your Username",
        'class': classes
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Your Password",
        'class': classes
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Your Password Confirmation",
        'class': classes
    }))


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={
        'placeholder': "Your Username",
        'class': classes
    }))
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput(attrs={
        'placeholder': "Your Password",
        'class': classes
    }))
