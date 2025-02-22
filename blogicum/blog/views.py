from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from blog.forms import UserEditForm
from blog.models import Post, Category
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
        return get_object_or_404(get_relevant_posts(Post.objects), id=post_id)


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
