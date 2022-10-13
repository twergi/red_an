from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from ribbon.models import SectionPost
from ribbon.utils import paginatePosts
from .forms import CustomUserCreationForm, UserLoginForm, UserEditForm, ProfileEditForm


def userView(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    posts_all = SectionPost.objects.filter(profile_id=profile.id)

    posts, page_range = paginatePosts(request, posts_all)

    context = {
        'username': username,
        'user': user,
        'profile': profile,
        'posts': posts,
        'page_range': page_range,
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
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
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
            user.email = form.cleaned_data.get('email')
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


@login_required(login_url='login')
def editUser(request):
    page = 'edit'
    user = request.user
    user_form = UserEditForm(instance=user)
    profile_form = ProfileEditForm(instance=user.profile)
    if request.method == 'POST':
        if 'edit_user' in request.POST:
            user_form = UserEditForm(request.POST, instance=user)
            profile_form = ProfileEditForm(request.POST, request.FILES, instance=user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('user', user.username)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'page': page,
    }
    return render(request, 'users/user_edit.html', context)


@login_required(login_url='login')
def deleteUser(request):
    page = 'delete'

    if request.method == 'POST':
        if 'delete_user' in request.POST:
            user = request.user
            user.delete()
            messages.success(request, 'User has been deleted')
            return redirect('login')

    context = {
        'page': page,
    }
    return render(request, 'users/user_edit.html', context)
