import os

from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, UpdateAPIView, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
import tweepy

from .serializers import UserSignupSerializer, UserMeSerializer, UserAuthSerializer, ChangePasswordSerializer, \
    UserProfileSerializer
from .models import User


class UserSignupView(CreateAPIView):
    queryset = ''
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSignupSerializer


class UserMeView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserMeSerializer

    def get_object(self):
        object = self.request.user
        self.check_object_permissions(self.request, object)
        return object


class UserLoginView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(UserMeSerializer(user).data)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        Token.objects.create(user=request.user)
        return Response({'message': 'User logged out successfully'})


class UserTwitterRequestTokenView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        auth = tweepy.OAuthHandler(os.environ.get("TWITTER_CONSUMER_KEY"), os.environ.get("TWITTER_CONSUMER_SECRET"))
        return Response({"redirect_link": auth.get_authorization_url()})


class PasswordChangeView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        object = self.request.user
        self.check_object_permissions(self.request, object)
        return object

    def update(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not object.check_password(serializer.data.get("current_password")):
                return Response({"current_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            object.set_password(serializer.data.get("new_password"))
            object.save()
            return Response(UserMeSerializer(object).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    lookup_field = "username"

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs["username"])
