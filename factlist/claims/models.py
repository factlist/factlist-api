from django.db import models
from django.utils import timezone

from factlist.users.models import User
from .constants import EVIDENCE_STATUS_CHOICES


class Claim(models.Model):
    text = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User)


class ClaimLink(models.Model):
    link = models.CharField(max_length=255)
    claim = models.ForeignKey(Claim, related_name='claim_links')

    def __unicode__(self):
        return self.text


class ClaimFile(models.Model):
    file = models.FileField(upload_to="files/claims/%Y/%m/%d/")
    claim = models.ForeignKey(Claim)


class Evidence(models.Model):
    claim = models.ForeignKey(Claim, related_name='evidences')
    text = models.CharField(max_length=255)
    status = models.CharField(max_length=100, choices=EVIDENCE_STATUS_CHOICES)
    created_by = models.ForeignKey(User)
    date_created = models.DateTimeField(default=timezone.now)


class EvidenceLink(models.Model):
    link = models.CharField(max_length=255)
    evidence = models.ForeignKey(Evidence, related_name='evidence_links')


class EvidenceFile(models.Model):
    file = models.FileField(upload_to="files/evidence/%Y/%m/%d/")
    evidence = models.ForeignKey(Evidence)
