from rest_framework import serializers

from factlist.users.serializers import MinimalUserSerializer
from factlist.claims.serializers import LinkSerializer
from .models import Topic, TopicLink, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            "id",
            "title",
            "created_at",
            "updated_at",
        )


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


class UpdateTopicSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
