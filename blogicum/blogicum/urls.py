from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import path, include, reverse_lazy
from django.views.generic import CreateView

handler404 = 'pages.views.custom_404'
handler500 = 'pages.views.custom_500'

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),

    path('auth/login/',
        auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    path('auth/logout/',
        auth_views.LogoutView.as_view(
        template_name='registration/logged_out.html'
    ), name='logout'),
    path('auth/password_change/',
        auth_views.PasswordChangeView.as_view(
           template_name='registration/password_change_form.html'
        ), name='password_change'),
    path('auth/password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
           template_name='registration/password_change_done.html'),
        name='password_change_done'),
    path('auth/password_reset/',
        auth_views.PasswordResetView.as_view(
           template_name='registration/password_reset_form.html'
        ), name='password_reset'),
    path('auth/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ), name='password_reset_done'),
    path('auth/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
           template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('auth/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
           template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
    path('auth/registration/',
        CreateView.as_view(
          template_name='registration/registration_form.html',
          form_class=UserCreationForm,
          success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),

    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls')),
    path('', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)
