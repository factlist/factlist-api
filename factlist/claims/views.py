from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response

from .models import Claim, Evidence
from .serializers import ClaimSerializer, EvidenceSerializer
from factlist.users.models import User


class ListAndCreateClaimView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClaimSerializer
    parser_classes = (MultiPartParser, JSONParser)

    def get_queryset(self):
        if self.request.GET.get('filter') is None:
            return Claim.objects.filter(active=True).order_by('-id')
        else:
            username = self.request.GET.get('filter').split(':')[1]
            user = User.objects.filter(username=username)
            if user.exists():
                return Claim.objects.filter(user=user)
            else:
                raise ValidationError('There is no user found with the given username')

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),


class ClaimView(RetrieveUpdateDestroyAPIView):
    serializer_class = ClaimSerializer
    parser_classes = (MultiPartParser, JSONParser)

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
    parser_classes = (MultiPartParser, JSONParser)

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
    parser_classes = (MultiPartParser, JSONParser)

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
