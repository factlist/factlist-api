from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(width_field="avatar_width", height_field="avatar_height", upload_to="users/images/%Y/%m/%d", null=True, blank=True)
    avatar_width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    avatar_height = models.PositiveIntegerField(editable=False, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
