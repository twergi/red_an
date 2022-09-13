from django.shortcuts import render, redirect
from .models import SectionPost, Section


def redirectRibbon(request):
    return redirect('ribbon')


def ribbonView(request):
    posts = SectionPost.objects.all()

    context = {
        'posts': posts
    }
    return render(request, 'ribbon/ribbon.html', context)


def sectionView(request, section_title):
    section = Section.objects.get(title=section_title)
    owner = section.sectionstaff.owner
    moderators = section.sectionstaff.moderators.all()

    posts = SectionPost.objects.filter(section_id=section.id)
    context = {
        'section': section,
        'posts': posts,
        'owner': owner,
        'moderators': moderators,
    }
    return render(request, 'ribbon/section.html', context)


def postView(request, section_title, post_id):
    post = SectionPost.objects.get(id=post_id)
    comments = post.comments_set.all()

    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'ribbon/post.html', context)
