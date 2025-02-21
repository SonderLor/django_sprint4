from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<slug:username>/', views.UserProfileView.as_view(), name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),
]
