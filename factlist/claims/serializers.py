from rest_framework import serializers

from factlist.users.serializers import SimpleUserSerializer
from .models import Claim, Evidence, File, Link


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('file', 'id')


class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = ('link', 'id')


class EvidenceSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    links = LinkSerializer(many=True, required=False)
    files = FileSerializer(many=True, required=False)

    class Meta:
        model = Evidence
        fields = (
            'id',
            'text',
            'status',
            'created_at',
            'updated_at',
            'deleted_at',
            'user',
            'links',
            'files',
        )

    def create(self, validated_data):
        evidence = Evidence(
            text=validated_data.pop('text'),
            status=validated_data.pop('status'),
            user=self.context['request'].user,
            claim_id=self.context['claim_id'],
        )
        evidence.save()
        if 'links' not in validated_data:
            pass
        else:
            links = validated_data.pop('links')
            for link in links:
                evidence_link = Link.objects.create(**link)
                evidence.links.add(evidence_link)
        if 'files' not in validated_data:
            pass
        else:
            files = validated_data.pop('links')
            for file in files:
                evidence_files = File.objects.create(**file)
                evidence.files.add(evidence_files)
        return evidence

    def update(self, instance, validated_data):
        instance.text = validated_data.pop('text')
        instance.status = validated_data.pop('status')
        instance.save()

        links = validated_data.pop('links')
        Link.objects.filter(evidence=instance).delete()
        for link in links:
            Link.objects.create(evidence=instance, **link)
        return instance


class ClaimSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    links = LinkSerializer(many=True, required=False)
    files = FileSerializer(many=True, required=False)

    class Meta:
        model = Claim
        fields = (
            'id',
            'text',
            'user',
            'links',
            'created_at',
            'updated_at',
            'deleted_at',
            'files',
            'true_count',
            'false_count',
            'inconclusive_count'
        )

    def create(self, validated_data):
        claim = Claim(
            text=validated_data.pop('text'),
            user=self.context['request'].user,
        )
        claim.save()
        if 'links' not in validated_data:
            pass
        else:
            links = validated_data.pop('links')
            for link in links:
                claim_link = Link.objects.create(**link)
                claim.links.add(claim_link)
        if 'files' not in validated_data:
            pass
        else:
            files = validated_data.pop('files')
            for file in files:
                claim_files = File.objects.create(**file)
                claim.files.add(claim_files)
        claim.save()
        return claim

    def update(self, instance, validated_data):
        instance.text = validated_data.pop('text')
        instance.save()

        links = validated_data.pop('links')
        Link.objects.filter(claim=instance).delete()
        for link in links:
            claim_link = Link.objects.create(claim=instance, **link)
            instance.links.add(claim_link)
        return instance
