from django.contrib.auth.backends import ModelBackend

from .models import User


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = User
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
