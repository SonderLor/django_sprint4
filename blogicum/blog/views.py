from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView

from blog.forms import UserEditForm
from blog.models import Post, Category
from blog.utils import get_relevant_posts

User = get_user_model()


def index(request):
    template = 'blog/index.html'

    post_list = get_relevant_posts(Post.objects)[0:5]

    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'

    post = get_object_or_404(get_relevant_posts(Post.objects), id=post_id)

    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(is_published=True), slug=category_slug
    )
    post_list = get_relevant_posts(
        category.posts.filter(category=category)
    )

    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)


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
