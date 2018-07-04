from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.cache import cache

from factlist.users.models import User
from .models import Claim, Evidence, File, Link
from .constants import EVIDENCE_STATUS


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'name', 'bio')


class UploadFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('image', 'id')


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = [
            "id",
            "image",
            "image_width",
            "image_height",
            "size",
            "extension",
            "name"
        ]


class LinkSerializer(serializers.ModelSerializer):
    embed = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ('link', 'embed')

    def get_embed(self, link):
        return cache.get(link.link)


class CreateEvidenceSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    conclusion = serializers.CharField(required=False)
    links = serializers.ListField(child=serializers.CharField(), max_length=6, required=False)
    files = serializers.ListField(child=serializers.IntegerField(), max_length=5, required=False)

    def validate(self, attrs):
        errors = {}
        if self.partial:
            return attrs

        if "text" not in attrs:
            errors["text"] = ["Evidence must contain a text"]

        if "conclusion" not in attrs:
            errors["conclusion"] = ["Evidence must contain a conclusion"]
        else:
            if attrs["conclusion"] not in EVIDENCE_STATUS:
                errors["conclusion"] = ["Evidence conclusion can be 'true', 'false' or 'inconclusive'."]

        if "links" not in attrs and "files" not in attrs:
            errors["links"] = ["Evidence must contain at least a file or link"]
            errors["files"] = ["Evidence must contain at least a file or link"]

        if "links" in attrs and "files" in attrs:
            if not attrs["links"] and not attrs["files"]:
                errors["links"] = ["Ensure this field has at least 1 elements."]
                errors["files"] = ["Ensure this field has at least 1 elements."]

        if errors:
            raise ValidationError(errors)
        return attrs


class EvidenceSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    files = FileSerializer(many=True)
    links = LinkSerializer(many=True)

    class Meta:
        model = Evidence
        fields = (
            'id',
            'text',
            'conclusion',
            'created_at',
            'updated_at',
            'deleted_at',
            'user',
            'links',
            'files',
        )


class CreateClaimSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    links = serializers.ListField(child=serializers.CharField(), max_length=6, required=False)
    files = serializers.ListField(child=serializers.IntegerField(), max_length=5, required=False)

    def validate(self, attrs):
        errors = {}
        if self.partial:
            return attrs

        if "text" not in attrs:
            errors["text"] = ["Claim must contain a text"]

        if "links" not in attrs and "files" not in attrs:
            errors["links"] = ["Claim must contain at least a file or link"]
            errors["files"] = ["Claim must contain at least a file or link"]

        if "links" in attrs and "files" in attrs:
            if not attrs["links"] and not attrs["files"]:
                errors["links"] = ["Ensure this field has at least 1 elements."]
                errors["files"] = ["Ensure this field has at least 1 elements."]

        if errors:
            raise ValidationError(errors)
        return attrs


class ClaimSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    links = LinkSerializer(many=True)
    files = FileSerializer(many=True)
    evidences = EvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = Claim
        fields = (
            'id',
            'text',
            'user',
            'created_at',
            'updated_at',
            'deleted_at',
            'evidences',
            'links',
            'files',
            'true_count',
            'false_count',
            'inconclusive_count'
        )


class UploadFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = [
            "id",
            "image",
        ]
