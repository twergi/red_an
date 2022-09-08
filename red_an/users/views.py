from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from ribbon.models import SectionPost


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
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'logged in successfully')
            return redirect(request.GET['next'] if 'next' in request.GET else 'ribbon')
        else:
            messages.error(request, 'username or password is incorrect')
    context = {'page': page}
    return render(request, 'users/login_register.html', context)


def registerUser(request):
    page = 'register'

    if request.user.is_authenticated:
        return redirect('user', request.user.username)

    context = {
        'page': page
    }
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('ribbon')
