from datetime import timedelta

from django.test import TestCase
from django.utils.crypto import get_random_string
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from .models import User, PasswordReset, EmailVerification


class UserTestMixin(object):
    def create_user_and_user_client(self):
        user = User.objects.create_user(
            username=get_random_string(10),
            email=get_random_string(10) + '@bobmail.com',
            password=get_random_string(10)
        )
        client = APIClient()
        client.default_format = 'json'
        client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        return user, client


class UserTestCase(TestCase, UserTestMixin):

    def test_register(self):
        user_client = APIClient()
        user_client.default_format = 'json'
        data = {
            'username': 'enis',
            'email': 'enis@factlist.org',
            'password': 'factlist_is_awesome',
            'name': 'Enis B. Tuysuz',
        }

        response = user_client.post('/api/v1/users/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'enis')
        self.assertEqual(response.data['email'], 'enis@factlist.org')

    def test_login(self):
        user_client = APIClient()
        user_client.default_format = 'json'
        data = {
            'username': 'enis',
            'email': 'enis@factlist.org',
            'password': 'factlist_is_awesome',
            'name': 'Enis B. Tuysuz',
        }
        response = user_client.post('/api/v1/users/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'email': 'enis@factlist.org',
            'password': 'factlist_is_awesome'
        }
        response = user_client.post('/api/v1/users/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        enis, enis_client = self.create_user_and_user_client()

        data = {
            "username": "enisbt",
            "name": "Enis B. Tuysuz",
            "bio": "Factlist is awesome",
            "email": "e@t.com"
        }
        response = enis_client.patch("/api/v1/users/me/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "enisbt")
        self.assertEqual(response.data["name"], "Enis B. Tuysuz")
        self.assertEqual(response.data["email"], "e@t.com")
        self.assertEqual(response.data["bio"], "Factlist is awesome")

    def test_change_password(self):
        user = User.objects.create_user(
            username=get_random_string(10),
            email=get_random_string(10) + '@bobmail.com',
            password="factlist_is_awesome"
        )
        client = APIClient()
        client.default_format = 'json'
        client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)

        data = {
            "current_password": "#this_password_is_wrong",
            "new_password": "#that_password_is_wrong"
        }
        response = client.patch("/api/v1/users/password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "current_password": "factlist_is_awesome",
            "new_password": "#factlist_is_awesome"
        }
        response = client.patch("/api/v1/users/password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_password_reset(self):
        enis, enis_client = self.create_user_and_user_client()

        password_reset = PasswordReset.objects.filter(user=enis)
        self.assertFalse(password_reset.exists())

        data = {
            "user_identifier": enis.username
        }
        response = enis_client.post("/api/v1/users/forgot_password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        password_reset = PasswordReset.objects.filter(user=enis)
        self.assertTrue(password_reset.exists())
        password_reset.delete()

        password_reset = PasswordReset.objects.filter(user=enis)
        self.assertFalse(password_reset.exists())

        data = {
            "user_identifier": enis.email
        }
        response = enis_client.post("/api/v1/users/forgot_password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        enis = User.objects.create_user(
            username="enis",
            password="#factlist",
            email=get_random_string(5) + '@bobmail.com',
            first_name=get_random_string(5),
            last_name=get_random_string(5),
            bio="Best backend developer of the world",
            verified=True,
        )
        enis_client = APIClient()
        enis_client.default_format = 'json'
        enis_client.credentials(HTTP_AUTHORIZATION='Token ' + enis.auth_token.key)

        data = {
            'email': enis.email,
            'password': '#factlist'
        }
        response = enis_client.post('/api/v1/users/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        password_reset = PasswordReset.objects.filter(user=enis)
        self.assertFalse(password_reset.exists())

        data = {
            "user_identifier": enis.username
        }
        response = enis_client.post("/api/v1/users/forgot_password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        password_reset = PasswordReset.objects.filter(user=enis)
        self.assertTrue(password_reset.exists())

        password_reset = password_reset.first()

        data = {
            "key": password_reset.key,
            "password": "1"
        }
        response = enis_client.post("/api/v1/users/change_password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        password_reset.until = timezone.now() - timedelta(hours=2)
        password_reset.save()

        data = {
            "key": password_reset.key,
            "password": "#factlist_is_awesome"
        }
        response = enis_client.post("/api/v1/users/change_password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        password_reset.until = timezone.now() + timedelta(hours=24)
        password_reset.save()

        data = {
            "key": password_reset.key,
            "password": "#factlist_is_awesome"
        }
        response = enis_client.post("/api/v1/users/change_password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'email': enis.email,
            'password': '#factlist_is_awesome'
        }
        response = enis_client.post('/api/v1/users/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_email(self):
        enis = User.objects.create_user(
            username="enis",
            password="#factlist",
            email=get_random_string(5) + '@bobmail.com',
            first_name=get_random_string(5),
            last_name=get_random_string(5),
            bio="Best backend developer of the world",
            verified=False,
        )
        enis_client = APIClient()
        enis_client.default_format = 'json'
        enis_client.credentials(HTTP_AUTHORIZATION='Token ' + enis.auth_token.key)

        user = User.objects.get(id=enis.id)
        self.assertFalse(user.verified)

        email_verification = EmailVerification.objects.filter(user=enis)
        self.assertTrue(email_verification.exists())

        data = {
            "key": email_verification.first().key
        }
        response = enis_client.post("/api/v1/users/verify_email/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(id=enis.id)
        self.assertTrue(user.verified)
