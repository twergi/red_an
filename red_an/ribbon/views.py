from django.shortcuts import render, redirect
from .models import SectionPost


def redirectRibbon(request):
    return redirect('ribbon')


def ribbonView(request):
    posts = SectionPost.objects.all()

    context = {
        'posts': posts
    }
    return render(request, 'ribbon/ribbon.html', context)


def postView(request, section_title, post_id):
    post = SectionPost.objects.get(id=post_id)
    comments = post.comments_set.all()

    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'ribbon/post.html', context)
