from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.utils import timezone
from rest_framework.authtoken.models import Token

from factlist.core.utils import send_sns


class User(AbstractUser):
    name = models.CharField(max_length=255)
    bio = models.CharField(max_length=160, null=True, blank=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(width_field="avatar_width", height_field="avatar_height", upload_to="users/images/%Y/%m/%d", null=True, blank=True)
    avatar_width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    avatar_height = models.PositiveIntegerField(editable=False, null=True, blank=True)
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(User, self).save(*args, **kwargs)
        if created:
            Token.objects.create(user=self)
            # Twitter users don't need to verify, that is why we check if the user is verified or not
            if not self.verified:
                key = get_random_string(50)
                while EmailVerification.objects.filter(key=key).exists():
                    key = get_random_string(50)
                EmailVerification.objects.create(key=key, user=self)
                message = {
                    "id": self.id,
                    "username": self.username,
                    "email": self.email,
                    "name": self.name,
                    "key": key
                }
                send_sns(message, "user-verification")

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'


class EmailVerification(models.Model):
    key = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User)


class PasswordReset(models.Model):
    key = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User)
    until = models.DateTimeField(default=timezone.now() + timedelta(hours=24))
