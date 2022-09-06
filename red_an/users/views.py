from django.shortcuts import render
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
