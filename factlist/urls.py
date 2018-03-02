from django.conf.urls import url, include
from django.contrib import admin

from factlist.embed.views import EmbedView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/v1/', include('factlist.users.urls')),
    url(r'^api/v1/', include('factlist.claims.urls')),
    url(r'^api/v1/embed/', EmbedView.as_view()),
]
