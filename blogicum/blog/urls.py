from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/<slug:username>/', views.user_profile_view, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('posts/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('posts/create/', views.post_create_view, name='create_post'),
    path('posts/<int:post_id>/edit/', views.post_update_view, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.post_delete_view, name='delete_post'),
    path('posts/<int:post_id>/comment/', views.comment_create_view, name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>', views.comment_update_view, name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>', views.comment_delete_view, name='delete_comment'),
    path('category/<slug:category_slug>/', views.category_posts_view, name='category_posts'),
]
