from django.core.cache import cache
from rest_framework import serializers

from factlist.users.serializers import MinimalUserSerializer
from factlist.claims.models import Link
from .models import Topic, TopicLink, Tag, LinkTag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            "id",
            "title",
            "created_at",
            "updated_at",
        )


class LinkSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    embed = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = (
            "id",
            "link",
            "created_at",
            "updated_at",
            "tags",
            'embed',
        )

    def get_tags(self, link):
        tag_ids = list(LinkTag.objects.filter(link=link).values_list("tag_id", flat=True))
        tags = Tag.objects.filter(id__in=tag_ids)
        tags = TagSerializer(tags, many=True)
        return tags.data

    def get_embed(self, link):
        return cache.get(link.link)


class TopicSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    links = LinkSerializer(many=True, source='topic_links')

    class Meta:
        model = Topic
        fields = (
            'id',
            'title',
            'user',
            'created_at',
            'updated_at',
            'tags',
            'links',
        )


class CreateTopicSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    link = serializers.CharField(required=True)


class TitleSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
