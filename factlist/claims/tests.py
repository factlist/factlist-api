from rest_framework import status
from django.test import TestCase

from factlist.users.tests import UserTestMixin
from factlist.claims.models import Claim, Evidence


class ClaimTestCase(TestCase, UserTestMixin):

    def test_post_claim(self):
        user, client = self.create_user_and_user_client()

        data = {
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        }
        response = client.post('/api/v1/claims/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'links': "['https://factlist.org']"
        }
        response = client.post('/api/v1/claims/', data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.')

    def test_get_list_of_claims(self):
        user, client = self.create_user_and_user_client()

        data = {
            'text': 'Factlist is a collaborative fact-checking platform.',
            'links': '["https://factlist.org"]'
        }
        response = client.post('/api/v1/claims/', data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get('/api/v1/claims/')
        self.assertEqual(response.data['count'], 1)

        data = {
            'text': 'Factlist is a collaborative fact-checking platform.',
            'links': "['https://factlist.org', 'https://lulxd.com']"
        }
        response = client.post('/api/v1/claims/', data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get('/api/v1/claims/')
        self.assertEqual(response.data['count'], 2)

    def test_get_a_claim(self):
        enis, enis_client = self.create_user_and_user_client()
        serafettin, serafettin_client = self.create_user_and_user_client()

        data = {
            'text': 'Factlist is a collaborative fact-checking platform.',
            'links': '["https://factlist.org"]'
        }
        response = enis_client.post('/api/v1/claims/', data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = enis_client.get('/api/v1/claims/%s/' % response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Factlist is a collaborative fact-checking platform.")

        response = serafettin_client.get('/api/v1/claims/%s/' % response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Factlist is a collaborative fact-checking platform.")

    def test_modify_a_claim(self):
        enis, enis_client = self.create_user_and_user_client()
        serafettin, serafettin_client = self.create_user_and_user_client()

        data = {
            'text': 'Factlist is a collaborative fact-checking platform.',
            'links': "['https://factlist.org']"
        }
        response = enis_client.post('/api/v1/claims/', data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'text': 'Factlist is a collaborative fact-checking platform.',
            'links': "['https://factlist.org', 'https://factlist.com/api/v1/']"
        }
        response = enis_client.patch('/api/v1/claims/%s/' % response.data['id'], data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = serafettin_client.patch('/api/v1/claims/%s/' % response.data['id'], data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_claim(self):
        enis, enis_client = self.create_user_and_user_client()
        serafettin, serafettin_client = self.create_user_and_user_client()

        data = {
            'text': 'Factlist is a collaborative fact-checking platform.',
            'links': '["https://factlist.org"]'
        }
        response = enis_client.post('/api/v1/claims/', data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        claim_id = response.data['id']

        response = serafettin_client.delete('/api/v1/claims/%s/' % claim_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = enis_client.delete('/api/v1/claims/%s/' % claim_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        claim = Claim.objects.get(pk=claim_id)
        self.assertFalse(claim.active)

    def test_post_an_evidence_to_claim(self):
        user, client = self.create_user_and_user_client()

        data = {
            "text": "Factlist is a collaborative fact-checking platform.",
            "links": '["https://twitter.com/factlist"]'
        }
        response = client.post('/api/v1/claims/', data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "text": "Factlist is a collaborative fact-checking platform.",
            "status": "true",
            "links": '["https://factlist.org"]'
        }
        response = client.post('/api/v1/claims/%s/evidences/' % response.data["id"], data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_modify_an_evidence(self):
        enis, enis_client = self.create_user_and_user_client()
        serafettin, serafettin_client = self.create_user_and_user_client()

        data = {
            'text': 'Factlist is a collaborative fact-checking platform.',
            'links': '["https://factlist.org"]'
        }
        response = serafettin_client.post('/api/v1/claims/', data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "text": "Factlist is a collaborative fact-checking platform.",
            "status": "true",
            "links": '["https://factlist.org"]'
        }

        response = enis_client.post('/api/v1/claims/%s/evidences/' % response.data["id"], data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        claim_id = response.data["id"]

        data = {
            "text": "Factlist is a collaborative fact-checking platform.",
            "status": "inconclusive",
            "links": '["https://factlist.org"]'
        }
        response = enis_client.patch('/api/v1/claims/%s/evidences/%s/' % (claim_id, response.data["id"]), data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = serafettin_client.patch('/api/v1/claims/%s/evidences/%s/' % (claim_id, response.data["id"]), data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_an_evidence(self):
        enis, enis_client = self.create_user_and_user_client()
        serafettin, serafettin_client = self.create_user_and_user_client()

        data = {
            'text': 'Factlist is a collaborative fact-checking platform.',
            'links': '["https://factlist.org"]',
        }
        response = serafettin_client.post('/api/v1/claims/', data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        claim_id = response.data["id"]

        data = {
            "text": "Factlist is a collaborative fact-checking platform.",
            "status": "true",
            "links": '["https://factlist.org"]'
        }

        response = enis_client.post('/api/v1/claims/%s/evidences/' % claim_id, data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        evidence_id = response.data["id"]

        response = serafettin_client.delete('/api/v1/claims/%s/evidences/%s/' % (claim_id, evidence_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = enis_client.delete('/api/v1/claims/%s/evidences/%s/' % (claim_id, evidence_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        evidence = Evidence.objects.get(pk=evidence_id)
        self.assertFalse(evidence.active)
