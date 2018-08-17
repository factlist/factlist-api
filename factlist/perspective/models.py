from django.db import models
from django.utils import timezone

from factlist.users.models import User
from factlist.claims.models import Link


class Topic(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'topics'

    def topic_links(self):
        link_ids = list(TopicLink.objects.filter(topic=self).values_list("link_id", flat=True))
        return Link.objects.filter(id__in=link_ids)


class Tag(models.Model):
    title = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="tags")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tags'


class LinkTag(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'link_tags'


class TopicLink(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'topic_links'
