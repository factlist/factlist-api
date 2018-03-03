from django.db import models
from django.utils import timezone

from factlist.users.models import User
from .constants import EVIDENCE_STATUS_CHOICES


class Link(models.Model):
    link = models.CharField(max_length=255)

    class Meta:
        db_table = 'links'


class File(models.Model):
    file = models.FileField(upload_to="files/claims/%Y/%m/%d/")

    class Meta:
        db_table = 'files'


class Claim(models.Model):
    text = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User)
    links = models.ManyToManyField(Link, db_table="claim_links")
    files = models.ManyToManyField(File, db_table="claim_files")

    class Meta:
        db_table = 'claims'


class Evidence(models.Model):
    claim = models.ForeignKey(Claim, related_name='evidences')
    text = models.CharField(max_length=255)
    status = models.CharField(max_length=100, choices=EVIDENCE_STATUS_CHOICES)
    created_by = models.ForeignKey(User)
    date_created = models.DateTimeField(default=timezone.now)
    links = models.ManyToManyField(Link, db_table="evidence_links")
    files = models.ManyToManyField(File, db_table="evidence_files")

    class Meta:
        db_table = 'evidences'
