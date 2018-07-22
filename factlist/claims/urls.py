from django.conf.urls import url

from .views import ClaimView, ListAndCreateClaimView, ListAndCreateEvidenceView, EvidenceView, UploadFileView, \
    SearchView

urlpatterns = [
    url(r'^files/$', UploadFileView.as_view()),
    url(r'^claims/$', ListAndCreateClaimView.as_view()),
    url(r'^claims/(?P<pk>[0-9]+)/$', ClaimView.as_view()),
    url(r'^claims/(?P<pk>[0-9]+)/evidences/$', ListAndCreateEvidenceView.as_view()),
    url(r'^claims/(?P<claim_pk>[0-9]+)/evidences/(?P<pk>[0-9]+)/$', EvidenceView.as_view()),
    url(r'^search/$', SearchView.as_view()),
]
