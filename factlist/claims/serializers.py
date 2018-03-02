from rest_framework import serializers

from factlist.users.serializers import SimpleUserSerializer
from .models import Claim, ClaimLink, ClaimFile, Evidence, EvidenceLink, EvidenceFile


class EvidenceFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = EvidenceFile
        fields = ('file', 'evidence', 'id')
        extra_kwargs = {'evidence': {'required': False}}


class EvidenceLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = EvidenceLink
        fields = ('link',)


class EvidenceSerializer(serializers.ModelSerializer):
    created_by = SimpleUserSerializer(read_only=True)
    links = EvidenceLinkSerializer(many=True)

    class Meta:
        model = Evidence
        fields = (
            'id',
            'text',
            'status',
            'date_created',
            'created_by',
            'links',
        )

    def create(self, validated_data):
        evidence = Evidence(
            text=validated_data.pop('text'),
            status=validated_data.pop('status'),
            created_by=self.context['request'].user,
            claim_id=self.context['claim_id'],
        )
        evidence.save()
        if 'evidence_links' not in validated_data:
            pass
        else:
            links = validated_data.pop('links')
            for link in links:
                EvidenceLink.objects.create(evidence=evidence, link=link)
        return evidence

    def update(self, instance, validated_data):
        instance.text = validated_data.pop('text')
        instance.status = validated_data.pop('status')
        instance.save()

        links = validated_data.pop('links')
        EvidenceLink.objects.filter(evidence=instance).delete()
        for link in links:
            EvidenceLink.objects.create(evidence=instance, **link)
        return instance


class ClaimFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClaimFile
        fields = ('file', 'claim', 'id')
        extra_kwargs = {'claim': {'required': False}}


class ClaimLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClaimLink
        fields = ('link',)


class ClaimSerializer(serializers.ModelSerializer):
    created_by = SimpleUserSerializer(read_only=True)
    links = ClaimLinkSerializer(many=True, required=False)
    files = ClaimFileSerializer(many=True, required=False)
    evidences = EvidenceSerializer(many=True, required=False)

    class Meta:
        model = Claim
        fields = (
            'id',
            'text',
            'created_by',
            'links',
            'date_created',
            'evidences',
            'files',
        )

    def create(self, validated_data):
        claim = Claim(
            text=validated_data.pop('text'),
            created_by=self.context['request'].user,
        )
        claim.save()
        if 'links' not in validated_data:
            pass
        else:
            links = validated_data.pop('links')
            for link in links:
                ClaimLink.objects.create(claim=claim, link=link)
        return claim

    def update(self, instance, validated_data):
        instance.text = validated_data.pop('text')
        instance.save()

        links = validated_data.pop('links')
        ClaimLink.objects.filter(claim=instance).delete()
        for link in links:
            ClaimLink.objects.create(claim=instance, **link)
        return instance
