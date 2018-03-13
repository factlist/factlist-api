from ast import literal_eval

from rest_framework import serializers
from django.core.cache import cache

from factlist.users.serializers import SimpleUserSerializer
from .models import Claim, Evidence, File, Link


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('file', 'id')


class LinkSerializer(serializers.ModelSerializer):
    embed = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ('link', 'id', 'embed')

    def get_embed(self, link):
        return cache.get(link.link)


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
        if 'links' in self.context['request'].POST:
            links = literal_eval(self.context['request'].POST['links'])
            for link in links:
                link_object = Link.objects.create(**link)
                evidence.links.add(link_object)
        else:
            pass
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
    evidences = EvidenceSerializer(many=True, read_only=True)

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
            'evidences',
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
        if 'links' in self.context['request'].POST:
            links = literal_eval(self.context['request'].POST['links'])
            for link in links:
                link_object = Link.objects.create(**link)
                claim.links.add(link_object)
        else:
            pass
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
