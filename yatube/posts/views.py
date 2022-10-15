# posts/views.py

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User
from .utils import paginator_

IMAGE_SIZE = settings.DEFAULT_IMAGE_SIZE


@cache_page(settings.CASHE_TIMEOUT, key_prefix='index_page')
def index(request):
    template = 'posts/index.html'
    posts_list = Post.objects.select_related(
        'author', 'group').all()
    page_obj = paginator_(request, posts_list)
    context = {
        'page_obj': page_obj,
        'image_size': IMAGE_SIZE
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    group_posts = group.posts.select_related(
        'author').all()
    page_obj = paginator_(request, group_posts)
    context = {
        'group': group,
        'page_obj': page_obj,
        'image_size': IMAGE_SIZE
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    # follow_flag:
    # (-1) - Подписка не может существовать
    # ( 0) - Подписки нет
    # ( 1) - Подписка существует
    follow_flag = -1
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        follow_obj = Follow.objects.filter(user=user, author=author)
        if not follow_obj.exists() and author != user:
            follow_flag = 0
        elif follow_obj.exists() and author != user:
            follow_flag = 1
    author_posts = author.posts.select_related(
        'group').all()
    page_obj = paginator_(request, author_posts)

    context = {
        'user_': author,
        'page_obj': page_obj,
        'follow_flag': follow_flag,
        'image_size': IMAGE_SIZE
    }
    return render(request, template, context)


def post_detail(request, post_id):

    if request.method != 'GET' and request.method != 'POST':
        return HttpResponseNotAllowed()

    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.select_related('author')
    form = CommentForm(request.POST or None)
    context = {
        'post': post,
        'comments': comments,
        'image_size': IMAGE_SIZE,
        'form': form
    }

    return render(request, template, context)


@login_required
def post_create(request):

    if request.method != 'GET' and request.method != 'POST':
        return HttpResponseNotAllowed()

    template = 'posts/create_post.html'
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    context = {'is_edit': False, 'form': form}

    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('posts:profile', request.user)

    return render(request, template, context)


@login_required
def post_edit(request, post_id):

    if request.method != 'GET' and request.method != 'POST':
        return HttpResponseNotAllowed(('GET', 'POST'))

    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        return redirect('posts:post_detail', post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    context = {'is_edit': True, 'form': form}

    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)

    return render(request, template, context)


@login_required
def add_comment(request, post_id):

    if request.method != 'GET' and request.method != 'POST':
        return HttpResponseNotAllowed(('GET', 'POST'))

    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    user = get_object_or_404(User, username=request.user.username)
    post_list = Post.objects.filter(author__following__user=user)
    page_obj = paginator_(request, post_list)
    context = {
        'page_obj': page_obj,
        'image_size': IMAGE_SIZE
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    user = get_object_or_404(User, username=request.user.username)
    follow_obj = Follow.objects.filter(user=user, author=author)
    can_follow = not follow_obj.exists() and user != author
    if can_follow:
        Follow.objects.create(user=user, author=author)
    return redirect('posts:profile', username=author.username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    user = get_object_or_404(User, username=request.user.username)
    follow_obj = Follow.objects.filter(user=user, author=author)
    can_unfollow = follow_obj.exists()
    if can_unfollow:
        follow_obj.delete()
    return redirect('posts:profile', username=author.username)
