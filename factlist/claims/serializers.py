from ast import literal_eval

from rest_framework import serializers
from django.core.cache import cache
from django.conf import settings

from factlist.users.serializers import SimpleUserSerializer
from .models import Claim, Evidence, File, Link


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('file',)


class LinkSerializer(serializers.ModelSerializer):
    embed = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ('link', 'embed')

    def get_embed(self, link):
        return cache.get(link.link)


class EvidenceSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    files = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

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
        if 'links' in self.context['request'].POST:
            links = literal_eval(self.context['request'].POST['links'])
            for link in links:
                link_object = Link.objects.create(link=link)
                evidence.links.add(link_object)
        if 'files' in self.context['request'].FILES:
            files = self.context["request"].FILES.getlist("files")
            for file in files:
                file_object = File.objects.create(file=file)
                evidence.files.add(file_object.id)
        else:
            pass
        evidence.save()
        return evidence

    def get_links(self, evidence):
        return list(evidence.links.all().values_list('link', flat=True))

    def get_files(self, evidence):
        files = list(evidence.files.all().values_list('file', flat=True))
        for x in range(len(files)):
            files[x] = "https://" + settings.AWS_S3_CUSTOM_DOMAIN + '/' + files[x]
        return files

    def update(self, instance, validated_data):
        instance.text = validated_data.pop('text')
        instance.status = validated_data.pop('status')
        instance.save()

        if 'links' in self.context['request'].POST:
            instance.links.all().delete()
            links = literal_eval(self.context['request'].POST['links'])
            for link in links:
                link_object = Link.objects.create(link=link)
                instance.links.add(link_object)
        if 'files' in self.context['request'].FILES:
            instance.files.all().delete()
            files = self.context["request"].FILES.getlist("files")
            for file in files:
                file_object = File.objects.create(file=file)
                instance.files.add(file_object.id)
        instance.save()
        return instance


class ClaimSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    files = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
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

    def create(self, validated_data):
        claim = Claim.objects.create(text=validated_data.pop('text'), user=self.context['request'].user)
        if 'links' in self.context['request'].POST:
            links = literal_eval(self.context['request'].POST['links'])
            for link in links:
                link_object = Link.objects.create(link=link)
                claim.links.add(link_object)
        if 'files' in self.context['request'].FILES:
            files = self.context["request"].FILES.getlist("files")
            for file in files:
                file_object = File.objects.create(file=file)
                claim.files.add(file_object.id)
        claim.save()
        return claim

    def get_links(self, claim):
        return list(claim.links.all().values_list('link', flat=True))

    def get_files(self, claim):
        files = list(claim.files.all().values_list('file', flat=True))
        for x in range(len(files)):
            files[x] = "https://" + settings.AWS_S3_CUSTOM_DOMAIN + '/' + files[x]
        return files

    def update(self, instance, validated_data):
        if 'text' in validated_data:
            instance.text = validated_data.pop('text')
        if 'status' in validated_data:
            instance.status = validated_data.pop('status')
        if 'links' in self.context['request'].POST:
            instance.links.all().delete()
            links = literal_eval(self.context['request'].POST['links'])
            for link in links:
                link_object = Link.objects.create(link=link)
                instance.links.add(link_object)
        if 'files' in self.context['request'].FILES:
            instance.files.all().delete()
            files = self.context["request"].FILES.getlist("files")
            for file in files:
                file_object = File.objects.create(file=file)
                instance.files.add(file_object.id)
        instance.save()
        return instance
