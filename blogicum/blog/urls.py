from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/<slug:username>/', views.UserProfileView.as_view(), name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('category/<slug:category_slug>/', views.CategoryPostsView.as_view(), name='category_posts'),
]
