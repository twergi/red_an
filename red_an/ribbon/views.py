from django.shortcuts import render
from .models import SectionPost


def ribbonView(request):
    posts = SectionPost.objects.all()

    context = {
        'posts': posts
    }
    return render(request, 'ribbon/ribbon.html', context)
