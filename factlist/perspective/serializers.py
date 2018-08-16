from rest_framework import serializers

from factlist.users.serializers import MinimalUserSerializer
from factlist.claims.serializers import LinkSerializer
from factlist.claims.models import Link
from .models import Issue, IssueLinks, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            "id",
            "title",
            "created_at",
            "updated_at",
        )


class IssueSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    links = LinkSerializer(many=True, source='issue_links')

    class Meta:
        model = Issue
        fields = (
            'id',
            'title',
            'user',
            'created_at',
            'updated_at',
            'tags',
            'links',
        )


class CreateIssueSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    link = serializers.CharField(required=True)


class UpdateIssueSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
