import os

from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, UpdateAPIView, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.core import exceptions
from django.contrib.auth import password_validation
from django.utils import timezone
from django.utils.crypto import get_random_string
import tweepy

from .serializers import UserSignupSerializer, UserMeSerializer, UserAuthSerializer, ChangePasswordSerializer, \
    UserProfileSerializer, ResetPasswordSerializer, ResetPasswordCreationSerializer, EmailVerificationSerializer
from .models import User, PasswordReset, EmailVerification


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


class PasswordResetCreationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordCreationSerializer(data=request.data)
        if serializer.is_valid():
            sender = None
            user = User.objects.filter(username=serializer.data["user_identifier"])
            if user.exists():
                sender = user.first()
            user = User.objects.filter(email=serializer.data["user_identifier"])
            if user.exists():
                sender = user.first()
            if sender:
                key = get_random_string(50)
                while PasswordReset.objects.filter(key=key):
                    key = get_random_string(50)
                PasswordReset.objects.create(user=sender, key=key)
            else:
                pass
            return Response(status=status.HTTP_200_OK)
        return Response([{"user_identifier": "This field is required"}], status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password_reset = PasswordReset.objects.filter(key=serializer.data["key"])
            if password_reset.exists():
                # Checking if the key is valid
                until = password_reset.first().until
                if timezone.now() > until:
                    return Response([{"key": "The key is expired"}], status=status.HTTP_400_BAD_REQUEST)
                user = password_reset.first().user
                # Password validation
                try:
                    password_validation.validate_password(serializer.data["password"])
                except exceptions.ValidationError:
                    return Response([{"password": "Invalid password"}], status=status.HTTP_400_BAD_REQUEST)
                user.set_password(serializer.data["password"])
                user.save()
                password_reset.delete()
                return Response({"Password changed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response([{"key": "The key doesn't exists"}], status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            verification = EmailVerification.objects.filter(key=serializer.data["key"])
            if verification.exists():
                user = verification.first().user
                user.verified = True
                user.save()
                return Response(status=status.HTTP_200_OK)
        return Response([{"key": "Verification key doesn't exists"}], status=status.HTTP_400_BAD_REQUEST)
