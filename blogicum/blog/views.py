from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView

from blog.forms import UserEditForm, PostForm, CommentForm
from blog.models import Post, Category, Comment
from blog.utils import get_relevant_posts

User = get_user_model()


class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"
    paginate_by = 10

    def get_queryset(self):
        return get_relevant_posts(Post.objects)


def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        post = get_object_or_404(get_relevant_posts(Post.objects), id=post_id)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    return render(request, "blog/detail.html", {
        "post": post, "form": form, "comments": comments
    })


@login_required
def post_create_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = PostForm()
    return render(request, "blog/create.html", {"form": form})


@login_required
def post_update_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect("blog:post_detail", post_id=post_id)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/create.html", {"form": form})


@login_required
def post_delete_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post.id)
    post.delete()
    return redirect("blog:profile", username=request.user.username)


@login_required
def comment_create_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post = post
            form.save()
            return redirect("blog:post_detail", post_id=post.id)
    else:
        form = CommentForm()
    return render(request, "blog/comment.html", {"form": form})


@login_required
def comment_update_view(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", post_id=post_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, "blog/comment.html", {
        "form": form, "comment": comment,
    })


@login_required
def comment_delete_view(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)
    if request.method == 'POST':
        comment.delete()
        return redirect("blog:post_detail", post_id=post_id)
    return render(request, "blog/comment.html", {"comment": comment})


def category_posts_view(request, category_slug):
    category = get_object_or_404(Category.objects.filter(is_published=True), slug=category_slug)
    posts = get_relevant_posts(category.posts.filter(category=category))
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/category.html", {
        "page_obj": page_obj, "category": category
    })


def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/profile.html", {
        "profile": user,
        "page_obj": page_obj,
    })


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse("blog:profile", kwargs={"username": user.username}))
    else:
        form = UserEditForm(instance=user)

    return render(request, "blog/user.html", {"form": form})
