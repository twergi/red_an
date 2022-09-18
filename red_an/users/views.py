from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from ribbon.models import SectionPost
from .forms import CustomUserCreationForm, UserLoginForm


def userView(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    posts = SectionPost.objects.filter(profile_id=profile.id)
    context = {
        'username': username,
        'user': user,
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'users/user.html', context)


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('user', request.user.username)

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username').lower()
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('user', username)
    else:
        form = UserLoginForm()
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def registerUser(request):
    page = 'register'

    if request.user.is_authenticated:
        return redirect('user', request.user.username)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            password = form.cleaned_data.get('password1')
            username = user.username
            user.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('user', username)

    else:
        form = CustomUserCreationForm()

    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('ribbon')
