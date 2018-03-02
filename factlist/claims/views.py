from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError

from .models import Claim, Evidence
from .serializers import ClaimSerializer, EvidenceSerializer, ClaimFileSerializer, EvidenceFileSerializer


class ListAndCreateClaimView(ListCreateAPIView):
    queryset = Claim.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClaimSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),


class ClaimView(RetrieveUpdateDestroyAPIView):
    serializer_class = ClaimSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_queryset(self):
        if self.request.method == "GET":
            return Claim.objects.filter(pk=self.kwargs["pk"])
        else:
            return Claim.objects.filter(pk=self.kwargs["pk"], created_by=self.request.user)


class ClaimFileView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClaimFileSerializer

    def perform_create(self, serializer):
        claim = Claim.objects.filter(pk=self.kwargs['pk'])
        if not claim.exists():
            raise ValidationError('Claim is not found for the file')
        serializer.save(claim=claim.first())


class ListAndCreateEvidenceView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EvidenceSerializer

    def get_serializer_context(self):
        return {"claim_id": self.kwargs["pk"], "request": self.request}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return Evidence.objects.filter(claim_id=self.kwargs["pk"])


class EvidenceView(RetrieveUpdateDestroyAPIView):
    serializer_class = EvidenceSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_queryset(self):
        if self.request.method == "GET":
            return Evidence.objects.filter(pk=self.kwargs["pk"])
        else:
            return Evidence.objects.filter(pk=self.kwargs["pk"], created_by=self.request.user)


class EvidenceFileView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EvidenceFileSerializer

    def perform_create(self, serializer):
        evidence = Evidence.objects.filter(pk=self.kwargs['evidence_pk'])
        if not evidence.exists():
            raise ValidationError('Claim is not found for the file')
        serializer.save(evidence=evidence.first())
