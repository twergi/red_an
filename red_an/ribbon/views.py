from django.shortcuts import render, redirect
from .utils import paginatePosts
from django.db.models import Q
from django.contrib.auth.models import User
from .models import SectionPost, Section
from django.contrib.auth.decorators import login_required
from .forms import SectionCreateForm, PostCreateForm, CommentForm


def redirectRibbon(request):
    return redirect('ribbon')


def ribbonView(request):
    search_posts = ''

    if request.GET.get('search_posts'):
        print(request.GET)
        search_posts = request.GET.get('search_posts')
        posts_all = SectionPost.objects.filter(
            Q(title__icontains=search_posts)
            | Q(content__icontains=search_posts)
        )
        try:
            search_username = User.objects.get(username=search_posts)
            posts_all |= SectionPost.objects.filter(profile_id=search_username.profile.id)
        except User.DoesNotExist:
            pass
    else:
        posts_all = SectionPost.objects.all()

    posts, page_range = paginatePosts(request, posts_all)

    context = {
        'posts': posts,
        'search_posts': search_posts,
        'page_range': page_range,
    }
    return render(request, 'ribbon/ribbon.html', context)


def sectionsView(request):
    all_sections = Section.objects.all()
    user = request.user

    context = {
        'user': user,
        'all_sections': all_sections,
    }

    if user.is_authenticated:
        user_sections = user.section_set.all()
        context['user_sections'] = user_sections

    return render(request, 'ribbon/sections.html', context)


def sectionView(request, section_title):
    section = Section.objects.get(title=section_title)
    user = request.user
    owner = section.owner
    posts = SectionPost.objects.filter(section_id=section.id)
    is_subscriber = user in section.subscribers.all()

    if request.method == 'POST':
        if 'subscription' in request.POST:
            if is_subscriber:
                section.subscribers.remove(user)
                return redirect('section', section_title)
            else:
                if user.is_authenticated:
                    section.subscribers.add(user)
                    return redirect('section', section_title)
                else:
                    return redirect('login')

    context = {
        'section': section,
        'posts': posts,
        'owner': owner,
        'is_subscriber': is_subscriber,
    }
    return render(request, 'ribbon/section.html', context)


@login_required(login_url='login')
def SectionCreate(request):
    form = SectionCreateForm()
    user = request.user
    page = 'create'
    if request.method == 'POST':
        form = SectionCreateForm(request.POST, request.FILES)
        if form.is_valid():
            section = form.save(commit=False)
            section.owner = user.profile
            section.save()
            return redirect('section', section.title)

    context = {
        'form': form,
        'user': user,
        'page': page,
    }
    return render(request, 'ribbon/section_create.html', context)


@login_required(login_url='login')
def SectionEdit(request, section_title):
    user = request.user
    section = Section.objects.get(title=section_title)

    if user.profile == section.owner:
        page = 'edit'
        form = SectionCreateForm(instance=section)

        if request.method == 'POST':
            form = SectionCreateForm(request.POST, request.FILES, instance=section)
            if form.is_valid():
                section = form.save()
                return redirect('section', section.title)

        context = {
            'page': page,
            'form': form,
            'section': section,
        }
        return render(request, 'ribbon/section_create.html', context)

    else:
        return redirect('sections')


@login_required(login_url='login')
def SectionDelete(request, section_title):
    user = request.user
    section = Section.objects.get(title=section_title)
    if user.profile == section.owner:
        page = 'delete'
        if request.method == 'POST':
            section.delete()
            return redirect('sections')

        context = {
            'page': page,
            'section': section,
        }
        return render(request, 'ribbon/section_create.html', context)
    else:
        return redirect('sections')


def postView(request, section_title, post_id):
    post = SectionPost.objects.get(id=post_id)
    comments = post.comment_set.all()
    form = CommentForm()

    if request.method == 'POST':
        if 'comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.profile_id = request.user.profile
                comment.section_post_id = post
                comment.save()
                return redirect('post', section_title, post_id)

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'ribbon/post.html', context)


@login_required(login_url='login')
def postCreate(request, section_title):
    form = PostCreateForm()
    user = request.user
    page = 'create'
    section = Section.objects.get(title=section_title)
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.section_id = section
            post.profile_id = user.profile
            post.save()
            return redirect('post', section.title, post.id)

    context = {
        'form': form,
        'user': user,
        'section': section,
        'page': page,
    }
    return render(request, 'ribbon/post_create.html', context)


@login_required(login_url='login')
def postEdit(request, section_title, post_id):
    user = request.user
    section = Section.objects.get(title=section_title)
    post = SectionPost.objects.get(id=post_id)

    if user.profile == post.profile_id:
        page = 'edit'
        form = PostCreateForm(instance=post)

        if request.method == 'POST':
            form = PostCreateForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save()
                return redirect('post', section.title, post.id)

        context = {
            'page': page,
            'form': form,
            'section': section,
            'post': post,
        }
        return render(request, 'ribbon/post_create.html', context)

    else:
        return redirect('post', section_title, post_id)


@login_required(login_url='login')
def postDelete(request, section_title, post_id):
    user = request.user
    section = Section.objects.get(title=section_title)
    post = SectionPost.objects.get(id=post_id)
    if user.profile == post.profile_id:
        page = 'delete'
        if request.method == 'POST':
            post.delete()
            return redirect('section', section_title)

        context = {
            'page': page,
            'section': section,
            'post': post,
        }
        return render(request, 'ribbon/post_create.html', context)
    else:
        return redirect('section', section_title)


def votePOST(request):
    if request.method == 'POST':
        print(request.POST)
    elif request.method == 'GET':
        return redirect('ribbon')
