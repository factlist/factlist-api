from django.contrib.auth.backends import ModelBackend
from rest_framework.exceptions import ValidationError

from .models import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = User
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            raise ValidationError({'email': ['There is no user with the given email']})
        else:
            if user.check_password(password):
                return user
        raise ValidationError({'password': ['Wrong password']})
