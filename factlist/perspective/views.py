from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from factlist.claims.models import Link
from factlist.claims.serializers import LinkSerializer
from .serializers import IssueSerializer, CreateIssueSerializer, UpdateIssueSerializer
from .models import Issue, IssueLinks, Tag


class ListAndCreateIssueView(ListCreateAPIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_queryset(self):
        return Issue.objects.filter().order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return IssueSerializer
        else:
            return CreateIssueSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateIssueSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = self.request.user
            issue = Issue.objects.create(
                user=user,
                title=serializer.data["title"],
            )
            if "link" in serializer.data:
                link_object = Link.objects.create(link=serializer.data["link"])
                IssueLinks.objects.create(link=link_object, issue=issue)
            return Response(IssueSerializer(issue).data, status=status.HTTP_201_CREATED)


class IssueView(RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_queryset(self):
        if self.request.method == "GET":
            return Issue.objects.filter(id=self.kwargs["pk"])
        else:
            return Issue.objects.filter(id=self.kwargs["pk"], user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return IssueSerializer
        else:
            return CreateIssueSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateIssueSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if "title" in serializer.data:
                instance.title = serializer.data["title"]
            return Response(IssueSerializer(instance).data, status=status.HTTP_200_OK)


class CreateLinkView(CreateAPIView):
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        IssueLinks.objects.create(issue_id=self.kwargs["pk"], link_id=serializer.data["id"])
