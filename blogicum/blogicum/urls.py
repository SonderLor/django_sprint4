from django.contrib import admin
from django.urls import path, include
from pages.views import custom_404, custom_500

handler404 = custom_404
handler500 = custom_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls')),
    path('', include('blog.urls')),
]
