from django.urls import path

from .views import ListAndCreateTopicView, TopicView, CreateLinkView

urlpatterns = [
    path('topics/', ListAndCreateTopicView.as_view()),
    path('topics/<int:pk>/', TopicView.as_view()),
    path('topics/<int:pk>/links/', CreateLinkView.as_view()),
]
