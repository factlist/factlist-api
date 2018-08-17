from django.urls import path

from .views import ListAndCreateIssueView, IssueView, CreateLinkView

urlpatterns = [
    path('issues/', ListAndCreateIssueView.as_view()),
    path('issues/<int:pk>/', IssueView.as_view()),
    path('issues/<int:pk>/links/', CreateLinkView.as_view()),
]
