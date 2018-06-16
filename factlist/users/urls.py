from django.conf.urls import url

from .views import UserLoginView, UserSignupView, UserMeView, UserLogoutView, UserTwitterRequestTokenView, \
    PasswordChangeView, UserView, PasswordResetView, PasswordResetCreationView

urlpatterns = [
    url(r'^users/login/$', UserLoginView.as_view(), name='login'),
    url(r'^users/register/$', UserSignupView.as_view(), name='signup'),
    url(r'^users/me/$', UserMeView.as_view(), name='me'),
    url(r'^users/logout/$', UserLogoutView.as_view()),
    url(r'^users/auth/twitter/$', UserTwitterRequestTokenView.as_view()),
    url(r'^users/password/$', PasswordChangeView.as_view()),
    url(r'^users/forgot_password/$', PasswordResetCreationView.as_view()),
    url(r'^users/change_password/$', PasswordResetView.as_view()),
    url(r'^users/(?P<username>.+)/$', UserView.as_view()),
]
