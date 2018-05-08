import os

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
import requests


class EmbedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.GET.get('link') is None:
            raise ValidationError('Missing the url argument')
        query = {
            "url": request.GET.get("link"),
            "key": os.environ.get("EMBEDLY_API_KEY"),
        }
        cache_control = cache.get(query['url'])
        if cache_control is not None:
            return Response(cache_control)
        else:
            r = requests.get("https://api.embedly.com/1/oembed", params=query)
            json_response = r.json()
            deleted_fields = [
                'provider_name',
                'provider_url',
                'author_name',
                'author_url',
                'version',
            ]
            if "error_message" in json_response:
                return Response({"message": "Invalid link"}, status=status.HTTP_404_NOT_FOUND)
            for field in deleted_fields:
                if field in json_response:
                    del json_response[field]
            cache.set(query['url'], json_response)
            return Response(json_response)
