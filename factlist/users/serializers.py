from rest_framework import serializers
from django.contrib.auth import authenticate, password_validation
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from the_big_username_blacklist import validate as validate_username

from .models import User
from factlist.claims.models import Claim, Evidence


class UserSignupSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'token', 'avatar', 'bio', 'name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        errors = {}
        username = validated_data.get("username")
        if not validate_username(username):
            errors["username"] = ["Invalid username"]

        password = validated_data.get('password')
        try:
            password_validation.validate_password(password)
        except:
            errors["password"] = ["Password is not strong enough"]

        if errors:
            raise exceptions.ValidationError(errors)
        user = User.objects.create_user(**validated_data)
        return user

    def get_token(self, user):
        token = Token.objects.get(user=user)
        return token.key


class UserMeSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    claims = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'token', 'claims', 'avatar', 'bio', 'name')

    def get_token(self, user):
        token = Token.objects.get(user=user)
        return token.key

    def get_claims(self, user):
        return Claim.objects.filter(user=user).count()


class UserAuthSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    class Meta:
        fields = ['email', 'password']

    def validate(self, attrs):
        username = attrs['email']
        password = attrs['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    claim_count = serializers.SerializerMethodField()
    evidence_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "bio",
            "claim_count",
            "evidence_count",
            "avatar",
        ]

    def get_claim_count(self, user):
        return Claim.objects.filter(user=user).count()

    def get_evidence_count(self, user):
        return Evidence.objects.filter(user=user).count()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordCreationSerializer(serializers.Serializer):
    user_identifier = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    key = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class EmailVerificationSerializer(serializers.Serializer):
    key = serializers.CharField(required=True)


class MinimalUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'name',
            'avatar',
        ]
