from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from .models import Claim, Evidence
from .serializers import ClaimSerializer, EvidenceSerializer, CreateClaimSerializer, CreateEvidenceSerializer
from factlist.users.models import User


class ListAndCreateClaimView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
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

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClaimSerializer
        else:
            return CreateClaimSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        self.perform_create(serializer)
        claim = Claim.objects.get(pk=serializer.data['id'])
        return Response(ClaimSerializer(claim).data, status=status.HTTP_201_CREATED)


class ClaimView(RetrieveUpdateDestroyAPIView):
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

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClaimSerializer
        else:
            return CreateClaimSerializer


class ListAndCreateEvidenceView(ListCreateAPIView):
    parser_classes = (MultiPartParser, JSONParser)

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['claim_id'] = self.kwargs['pk']
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, claim=self.kwargs['pk'])

    def get_queryset(self):
        return Evidence.objects.filter(claim_id=self.kwargs["pk"], active=True)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EvidenceSerializer
        else:
            return CreateEvidenceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        self.perform_create(serializer)
        evidence = Evidence.objects.get(pk=serializer.data['id'])
        return Response(EvidenceSerializer(evidence).data, status=status.HTTP_201_CREATED)


class EvidenceView(RetrieveUpdateDestroyAPIView):
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

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EvidenceSerializer
        else:
            return CreateEvidenceSerializer
