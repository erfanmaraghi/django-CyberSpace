from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('core:index')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                nextURL = request.GET.get('next', '')
                if nextURL:
                    return redirect(nextURL)
                return redirect('core:index')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required()
def logout_view(request):
    logout(request)
    return redirect("core:index")


@login_required()
def delete_view(request):
    request.user.delete()
    return redirect('core:index')
