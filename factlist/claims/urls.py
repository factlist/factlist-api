from django.urls import path

from .views import ClaimView, ListAndCreateClaimView, ListAndCreateEvidenceView, EvidenceView, UploadFileView, \
    SearchView

urlpatterns = [
    path('files/', UploadFileView.as_view()),
    path('claims/', ListAndCreateClaimView.as_view()),
    path('claims/<int:pk>/', ClaimView.as_view()),
    path('claims/<int:pk>/evidences/', ListAndCreateEvidenceView.as_view()),
    path('claims/<int:claim_pk>/evidences/<int:pk>/', EvidenceView.as_view()),
    path('search/', SearchView.as_view()),
]
