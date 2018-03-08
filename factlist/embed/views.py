import os

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import requests


class EmbedView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        query = {
            "url": request.GET.get("link"),
            "key": os.environ.get("EMBEDLY_API_KEY"),
        }
        '''
        TODO: Remove
                - provider name
                - provider url
                - author name
                - author url
                - version
              from the embed.ly response
        '''
        cache_control = cache.get(query['url'])
        if cache_control is not None:
            return Response(cache_control)
        else:
            r = requests.get("https://api.embedly.com/1/oembed", params=query)
            cache.set(query['url'], r.json())
            return Response(r.json())
