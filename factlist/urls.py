from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/v1/', include('factlist.users.urls')),
    url(r'^api/v1/', include('factlist.claims.urls')),
]
