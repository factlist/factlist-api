from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from factlist.users.serializers import SimpleUserSerializer
from .models import Claim, ClaimLink, ClaimFile, Evidence, EvidenceLink, EvidenceFile


class EvidenceFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = EvidenceFile
        fields = ('file', 'id')


class EvidenceLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = EvidenceLink
        fields = ('text', "id")


class EvidenceSerializer(serializers.ModelSerializer):
    created_by = SimpleUserSerializer(read_only=True)
    evidence_links = EvidenceLinkSerializer(many=True)
    evidence_files = EvidenceFileSerializer(many=True)

    class Meta:
        model = Evidence
        fields = (
            'id',
            'text',
            'status',
            'date_created',
            'created_by',
            'evidence_links',
        )

    def create(self, validated_data):
        if "evidence_links" not in validated_data and "evidence_files" not in validated_data:
            raise ValidationError("Files and links cannot be empty at the same time")
        links = validated_data.pop('evidence_links')
        evidence = Evidence(
            text=validated_data.pop('text'),
            status=validated_data.pop('status'),
            created_by=self.context["request"].user,
            claim_id=self.context["claim_id"],
        )
        evidence.save()
        for link in links:
            EvidenceLink.objects.create(evidence=evidence, **link)
        return evidence

    def update(self, instance, validated_data):
        instance.text = validated_data.pop("text")
        instance.status = validated_data.pop("status")
        instance.save()

        links = validated_data.pop("evidence_links")
        EvidenceLink.objects.filter(evidence=instance).delete()
        for link in links:
            EvidenceLink.objects.create(evidence=instance, **link)
        return instance


class ClaimFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClaimFile
        fields = ("file",)


class ClaimLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClaimLink
        fields = ('text',)


class ClaimSerializer(serializers.ModelSerializer):
    created_by = SimpleUserSerializer(read_only=True)
    claim_links = ClaimLinkSerializer(many=True, required=False)
    claim_files = ClaimFileSerializer(many=True, required=False)
    evidences = EvidenceSerializer(many=True, required=False)

    class Meta:
        model = Claim
        fields = (
            'id',
            'text',
            'created_by',
            'claim_links',
            'date_created',
            'evidences',
            'claim_files',
        )

    def create(self, validated_data):
        claim = Claim(
            text=validated_data.pop("text"),
            created_by=self.context["request"].user,
        )
        claim.save()
        if "claim_links" not in validated_data:
            pass
        else:
            links = validated_data.pop('claim_links')
            for link in links:
                ClaimLink.objects.create(claim=claim, text=link)
        return claim

    def update(self, instance, validated_data):
        instance.text = validated_data.pop("text")
        instance.save()

        links = validated_data.pop("claim_links")
        ClaimLink.objects.filter(claim=instance).delete()
        for link in links:
            ClaimLink.objects.create(claim=instance, **link)
        return instance
