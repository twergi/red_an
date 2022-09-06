from django.shortcuts import render
from django.contrib.auth.models import User


def userView(request, username):
    user = User.objects.get(username=username)
    profile = user.profile

    context = {
        'username': username,
        'user': user,
        'profile': profile,
    }
    return render(request, 'users/user.html', context)
