from django.db import models
from django.utils import timezone

from factlist.users.models import User
from .constants import EVIDENCE_STATUS_CHOICES


class Link(models.Model):
    link = models.CharField(max_length=255)

    class Meta:
        db_table = 'links'


class File(models.Model):
    file = models.FileField(upload_to="files/%Y/%m/%d/", max_length=400)

    class Meta:
        db_table = 'files'


class Claim(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User)
    links = models.ManyToManyField(Link, db_table="claim_links")
    files = models.ManyToManyField(File, db_table="claim_files")

    @property
    def true_count(self):
        evidences = Evidence.objects.filter(claim=self, status="true")
        if evidences.exists():
            return evidences.count()
        else:
            return 0

    @property
    def false_count(self):
        evidences = Evidence.objects.filter(claim=self, status="false")
        if evidences.exists():
            return evidences.count()
        else:
            return 0

    @property
    def inconclusive_count(self):
        evidences = Evidence.objects.filter(claim=self, status="inconclusive")
        if evidences.exists():
            return evidences.count()
        else:
            return 0

    class Meta:
        db_table = 'claims'


class Evidence(models.Model):
    claim = models.ForeignKey(Claim, related_name='evidences')
    text = models.TextField()
    status = models.CharField(max_length=100, choices=EVIDENCE_STATUS_CHOICES)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now)
    links = models.ManyToManyField(Link, db_table="evidence_links")
    files = models.ManyToManyField(File, db_table="evidence_files")

    class Meta:
        db_table = 'evidences'
