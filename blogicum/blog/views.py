from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

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


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_object(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        if self.request.user == post.author:
            return post

        return get_object_or_404(get_relevant_posts(Post.objects), id=post_id)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:profile", kwargs={"username": self.request.user.username})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        if post.author != self.request.user:
            return redirect("blog:post_detail", post_id=post.id)
        return post

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.object.id})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs["post_id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.kwargs["post_id"]})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def get_object(self, queryset=None):
        comment = get_object_or_404(Comment, id=self.kwargs["comment_id"])
        if comment.author != self.request.user:
            return redirect("blog:post_detail", post_id=comment.post.id)
        return comment

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.object.post.id})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        comment = get_object_or_404(Comment, id=self.kwargs["comment_id"])
        if comment.author != self.request.user:
            return redirect("blog:post_detail", post_id=comment.post.id)
        return comment

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.object.post.id})


class CategoryPostsView(ListView):
    model = Post
    template_name = "blog/category.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        category = get_object_or_404(Category.objects.filter(is_published=True), slug=category_slug)
        return get_relevant_posts(category.posts.filter(category=category))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(Category.objects.filter(is_published=True),
                                                slug=self.kwargs.get("category_slug"))
        return context


class UserProfileView(DetailView):
    model = User
    template_name = "blog/profile.html"
    context_object_name = "profile"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        posts = Post.objects.filter(author=user).order_by("-created_at")
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get("page")
        context["page_obj"] = paginator.get_page(page_number)
        context["is_owner"] = self.request.user == user
        context["edit_profile_url"] = reverse("blog:edit_profile") if context["is_owner"] else None
        context["password_change_url"] = reverse("password_change") if context["is_owner"] else None
        return context


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
