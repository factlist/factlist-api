from django.test import TestCase
from rest_framework import status

from factlist.users.tests import UserTestMixin


class PerspectiveTestCase(TestCase, UserTestMixin):

    def test_create_issue(self):
        user, client = self.create_user_and_user_client()

        data = {
            'title': 'Test issue',
            'link': "https://github.com",
        }
        response = client.post('/api/v1/issues/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test issue")

    def test_get_list_of_issues(self):
        user, client = self.create_user_and_user_client()

        data = {
            'title': 'Test issue',
            'link': "https://github.com",
        }
        response = client.post('/api/v1/issues/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get('/api/v1/issues/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        data = {
            'title': 'Test issue2',
            'link': "https://github.com",
        }
        response = client.post('/api/v1/issues/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get('/api/v1/issues/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_get_an_issue(self):
        user, client = self.create_user_and_user_client()

        data = {
            'title': 'Test issue',
            'link': "https://github.com",
        }
        response = client.post('/api/v1/issues/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get("/api/v1/issues/%s/" % response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test issue")

    def test_update_an_issue(self):
        enis, enis_client = self.create_user_and_user_client()
        ali, ali_client = self.create_user_and_user_client()

        data = {
            'title': 'Test issue',
            'link': "https://github.com",
        }
        response = enis_client.post('/api/v1/issues/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "title": "Test issue edit"
        }
        response = enis_client.patch('/api/v1/issues/%s/' % response.data["id"], data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            "title": "Test issue edit"
        }
        response = ali_client.patch('/api/v1/issues/%s/' % response.data["id"], data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_an_issue(self):
        enis, enis_client = self.create_user_and_user_client()
        ali, ali_client = self.create_user_and_user_client()

        data = {
            'title': 'Test issue',
            'link': "https://github.com",
        }
        response = enis_client.post('/api/v1/issues/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        issue_id = response.data["id"]

        response = ali_client.delete('/api/v1/issues/%s/' % issue_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = enis_client.delete('/api/v1/issues/%s/' % issue_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_a_link(self):
        enis, enis_client = self.create_user_and_user_client()
        ali, ali_client = self.create_user_and_user_client()

        data = {
            'title': 'Test issue',
            'link': "https://github.com",
        }
        response = enis_client.post('/api/v1/issues/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        issue_id = response.data["id"]

        data = {
            "link": "https://twitter.com"
        }
        response = enis_client.post("/api/v1/issues/%s/links/" % issue_id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
