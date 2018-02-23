from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Claim, Evidence
from .serializers import ClaimSerializer, EvidenceSerializer


class ListAndCreateClaimView(ListCreateAPIView):
    queryset = Claim.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClaimSerializer


class ClaimView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClaimSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Claim.objects.filter(pk=self.kwargs["pk"])
        else:
            return Claim.objects.filter(pk=self.kwargs["pk"], created_by=self.request.user)


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
    permission_classes = [IsAuthenticated]
    serializer_class = EvidenceSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Evidence.objects.filter(pk=self.kwargs["pk"])
        else:
            return Evidence.objects.filter(pk=self.kwargs["pk"], created_by=self.request.user)
