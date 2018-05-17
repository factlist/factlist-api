from django.conf.urls import url

from .views import UserLoginView, UserSignupView, UserMeView, UserLogoutView

urlpatterns = [
    url(r'^users/login/$', UserLoginView.as_view(), name='login'),
    url(r'^users/register/$', UserSignupView.as_view(), name='signup'),
    url(r'^users/me/$', UserMeView.as_view(), name='me'),
    url(r'^users/logout/$', UserLogoutView.as_view()),
]
