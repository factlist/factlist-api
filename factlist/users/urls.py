from django.urls import path

from .views import UserLoginView, UserSignupView, UserMeView, UserLogoutView, UserTwitterRequestTokenView, \
    PasswordChangeView, UserView, PasswordResetView, PasswordResetCreationView, EmailVerificationView, TwitterLoginView

urlpatterns = [
    path('users/login/', UserLoginView.as_view(), name='login'),
    path('users/login/twitter/', TwitterLoginView.as_view()),
    path('users/register/', UserSignupView.as_view(), name='signup'),
    path('users/me/', UserMeView.as_view(), name='me'),
    path('users/logout/', UserLogoutView.as_view()),
    path('users/auth/twitter/', UserTwitterRequestTokenView.as_view()),
    path('users/password/', PasswordChangeView.as_view()),
    path('users/forgot_password/', PasswordResetCreationView.as_view()),
    path('users/change_password/', PasswordResetView.as_view()),
    path('users/verify_email/', EmailVerificationView.as_view()),
    path('users/<slug:username>/', UserView.as_view()),
]
