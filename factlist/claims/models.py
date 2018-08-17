from django.db import models
from django.utils import timezone

from factlist.users.models import User
from .constants import EVIDENCE_STATUS_CHOICES


class Link(models.Model):
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'links'


class File(models.Model):
    """
    Only accepting images for now
    """
    image = models.ImageField(width_field="image_width", height_field="image_height", upload_to="claims/images/%Y/%m/%d")
    image_width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    image_height = models.PositiveIntegerField(editable=False, null=True, blank=True)
    size = models.PositiveIntegerField(null=True, blank=True)
    extension = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'files'


class Claim(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    links = models.ManyToManyField(Link, db_table="claim_links")
    files = models.ManyToManyField(File, db_table="claim_files")

    @property
    def true_count(self):
        evidences = Evidence.objects.filter(claim=self, conclusion="true", active=True)
        if evidences.exists():
            return evidences.count()
        else:
            return 0

    @property
    def false_count(self):
        evidences = Evidence.objects.filter(claim=self, conclusion="false", active=True)
        if evidences.exists():
            return evidences.count()
        else:
            return 0

    @property
    def inconclusive_count(self):
        evidences = Evidence.objects.filter(claim=self, conclusion="inconclusive", active=True)
        if evidences.exists():
            return evidences.count()
        else:
            return 0

    class Meta:
        db_table = 'claims'
        ordering = ('-id',)

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

    def active_evidences(self):
        return Evidence.objects.filter(claim=self, active=True)


class Evidence(models.Model):
    claim = models.ForeignKey(Claim, related_name='evidences', on_delete=models.CASCADE)
    text = models.TextField()
    conclusion = models.CharField(max_length=100, choices=EVIDENCE_STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
