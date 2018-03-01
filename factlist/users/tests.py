from django.test import TestCase
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient
from rest_framework import status

from .models import User


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
        }
        response = user_client.post('/api/v1/users/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'email': 'enis@factlist.org',
            'password': 'factlist_is_awesome'
        }
        response = user_client.post('/api/v1/users/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
