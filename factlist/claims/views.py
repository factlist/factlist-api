from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from .models import Claim, Evidence, Link, File
from .serializers import ClaimSerializer, EvidenceSerializer, CreateClaimSerializer, CreateEvidenceSerializer, \
    UploadFileSerializer
from factlist.users.models import User
from .constants import EVIDENCE_STATUS
# from factlist.users.permissions import IsVerified


class ListAndCreateClaimView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.GET.get('filter') is None:
            return Claim.objects.filter(active=True).order_by('-id')
        else:
            username = self.request.GET.get('filter').split(':')[1]
            user = User.objects.filter(username=username)
            if user.exists():
                return Claim.objects.filter(user=user)
            else:
                raise ValidationError({'filter': ['There is no user with given username']})

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClaimSerializer
        else:
            return CreateClaimSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateClaimSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = self.request.user
            claim = Claim.objects.create(text=serializer.data["text"], user=user)
            if "links" in serializer.data:
                links = serializer.data["links"]
                for link in links:
                    link_object = Link.objects.create(link=link)
                    claim.links.add(link_object)
            if "files" in serializer.data:
                files = serializer.data["files"]
                for file in files:
                    try:
                        file_object = File.objects.get(id=file)
                    except File.DoesNotExist:
                        raise ValidationError({'files': ['Invalid file']})
                    claim.files.add(file_object)
            claim.save()
            return Response(ClaimSerializer(claim).data, status=status.HTTP_201_CREATED)


class ClaimView(RetrieveUpdateDestroyAPIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_queryset(self):
        if self.request.method == "GET":
            return Claim.objects.filter(pk=self.kwargs["pk"], active=True)
        else:
            return Claim.objects.filter(pk=self.kwargs["pk"], user=self.request.user, active=True)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClaimSerializer
        else:
            return CreateClaimSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = CreateClaimSerializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            if "text" in serializer.data:
                instance.text = serializer.data["text"]
            if "links" in serializer.data:
                links = serializer.data["links"]
                instance.links.all().delete()
                for link in links:
                    link_object = Link.objects.create(link=link)
                    instance.links.add(link_object)
            if "files" in serializer.data:
                files = serializer.data["files"]
                instance.files.all().delete()
                for file in files:
                    try:
                        file_object = File.objects.get(id=file)
                    except File.DoesNotExist:
                        raise ValidationError({'files': ['Invalid file']})
                    instance.files.add(file_object)
            instance.save()
            return Response(ClaimSerializer(instance).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Claim deleted successfully"}, status=status.HTTP_200_OK)


class ListAndCreateEvidenceView(ListCreateAPIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['claim_id'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return Evidence.objects.filter(claim_id=self.kwargs["pk"], active=True)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EvidenceSerializer
        else:
            return CreateEvidenceSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateEvidenceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = self.request.user
            claim_id = self.kwargs["pk"]
            evidence = Evidence.objects.create(
                text=serializer.data["text"],
                user=user,
                claim_id=claim_id,
                conclusion=serializer.data["conclusion"]
            )
            if "links" in serializer.data:
                links = serializer.data["links"]
                for link in links:
                    link_object = Link.objects.create(link=link)
                    evidence.links.add(link_object)
            if "files" in serializer.data:
                files = serializer.data["files"]
                for file in files:
                    try:
                        file_object = File.objects.get(id=file)
                    except File.DoesNotExist:
                        raise ValidationError({'files': ['Invalid file']})
                    evidence.files.add(file_object)
            evidence.save()
            return Response(EvidenceSerializer(evidence).data, status=status.HTTP_201_CREATED)


class EvidenceView(RetrieveUpdateDestroyAPIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_queryset(self):
        if self.request.method == "GET":
            return Evidence.objects.filter(pk=self.kwargs["pk"], active=True)
        else:
            return Evidence.objects.filter(pk=self.kwargs["pk"], user=self.request.user, active=True)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EvidenceSerializer
        else:
            return CreateEvidenceSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = CreateEvidenceSerializer(data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            if "text" in serializer.data:
                instance.text = serializer.data["text"]
            if "conclusion" in serializer.data:
                if serializer.data["conclusion"] not in EVIDENCE_STATUS:
                    raise ValidationError({"conclusion": ["Evidence conclusion can be 'true', 'false' or 'inconclusive'."]})
                instance.conclusion = serializer.data["conclusion"]
            if "links" in serializer.data:
                links = serializer.data["links"]
                instance.links.all().delete()
                for link in links:
                    link_object = Link.objects.create(link=link)
                    instance.links.add(link_object)
            if "files" in serializer.data:
                files = serializer.data["files"]
                instance.files.all().delete()
                for file in files:
                    try:
                        file_object = File.objects.get(id=file)
                    except File.DoesNotExist:
                        raise ValidationError({'files': ['Invalid file']})
                    instance.files.add(file_object)
            instance.save()
            return Response(EvidenceSerializer(instance).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Evidence deleted successfully"}, status=status.HTTP_200_OK)


class UploadFileView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadFileSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        size = request.data["image"].size
        name = request.data["image"].name
        extension = name.split(".")[-1]
        file_object = File.objects.get(id=response.data["id"])
        file_object.size = size
        file_object.name = name
        file_object.extension = extension
        file_object.save()
        return response


class SearchView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ClaimSerializer

    def get_queryset(self):
        if self.request.GET.get('query') is None:
            return Response({"query": ['You need to search with a query']}, status=status.HTTP_400_BAD_REQUEST)
        return Claim.objects.filter(text__icontains=self.request.GET.get('query'))
