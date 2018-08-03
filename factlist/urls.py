from django.urls import path, include
from django.contrib import admin

from factlist.embed.views import EmbedView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('factlist.users.urls')),
    path('api/v1/', include('factlist.claims.urls')),
    path('api/v1/embed/', EmbedView.as_view()),
]
