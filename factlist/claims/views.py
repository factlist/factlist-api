from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Claim, Evidence
from .serializers import ClaimSerializer, EvidenceSerializer, FileSerializer


class ListAndCreateClaimView(ListCreateAPIView):
    queryset = Claim.objects.filter(active=True)
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
            return Claim.objects.filter(pk=self.kwargs["pk"], active=True)
        else:
            return Claim.objects.filter(pk=self.kwargs["pk"], user=self.request.user, active=True)


class ListAndCreateEvidenceView(ListCreateAPIView):
    serializer_class = EvidenceSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_serializer_context(self):
        return {"claim_id": self.kwargs["pk"], "request": self.request}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Evidence.objects.filter(claim_id=self.kwargs["pk"], active=True)


class EvidenceView(RetrieveUpdateDestroyAPIView):
    serializer_class = EvidenceSerializer

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
