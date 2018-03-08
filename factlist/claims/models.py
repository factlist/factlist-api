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
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User)
    links = models.ManyToManyField(Link, db_table="claim_links")
    files = models.ManyToManyField(File, db_table="claim_files")

    @property
    def true_count(self):
        evidences = Evidence.objects.filter(claim=self, status="true", active=True)
        if evidences.exists():
            return evidences.count()
        else:
            return 0

    @property
    def false_count(self):
        evidences = Evidence.objects.filter(claim=self, status="false", active=True)
        if evidences.exists():
            return evidences.count()
        else:
            return 0

    @property
    def inconclusive_count(self):
        evidences = Evidence.objects.filter(claim=self, status="inconclusive", active=True)
        if evidences.exists():
            return evidences.count()
        else:
            return 0

    class Meta:
        db_table = 'claims'

    def update(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.save()
        super(Claim, self).update(self, *args, **kwargs)

    def delete(self):
        self.deleted_at = timezone.now()
        self.active = False
        self.save()
        evidences = Evidence.objects.filter(claim=self, active=True)
        for evidence in evidences:
            evidence.active = False
            evidence.save()


class Evidence(models.Model):
    claim = models.ForeignKey(Claim, related_name='evidences')
    text = models.TextField()
    status = models.CharField(max_length=100, choices=EVIDENCE_STATUS_CHOICES)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    links = models.ManyToManyField(Link, db_table="evidence_links")
    files = models.ManyToManyField(File, db_table="evidence_files")

    class Meta:
        db_table = 'evidences'

    def update(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.save()
        super(Evidence, self).update(self, *args, **kwargs)

    def delete(self):
        self.deleted_at = timezone.now()
        self.active = False
        self.save()
