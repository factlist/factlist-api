import json
import io

from django.core.management.base import BaseCommand
from django.core import files
from django.utils.crypto import get_random_string
import requests

from factlist.claims.models import Evidence, Claim, File, Link
from factlist.users.models import User


class Command(BaseCommand):
    help = "Seed database management command"

    def handle(self, *args, **options):

        mock_user = User.objects.create_user(
            username="serafettin",
            email="serafettin@factlist.org",
            password="#factlist2018",
        )
        with open("./factlist/core/management/commands/seed.json") as json_raw:
            json_file = json.load(json_raw)
            for key, value in json_file.items():
                claim = Claim(
                    text=value["text"],
                    user=mock_user,
                )
                claim.save()
                if not "evidences" in value:
                    pass
                else:
                    for evidence in value["evidences"]:
                        evidence_object = Evidence(
                            claim=claim,
                            text=evidence["text"],
                            user=mock_user,
                            conclusion=evidence["conclusion"],
                            created_at=evidence["created_at"],
                        )
                        evidence_object.save()
                        if evidence["links"] is None:
                            pass
                        else:
                            for link in evidence["links"]:
                                link_object = Link.objects.create(link=link["url"], user=self.request.user)
                                evidence_object.links.add(link_object)
                        evidence_object.save()
                for file in value["files"]:
                    url = file["source"]
                    file_object = File()
                    file_object.file = url
                    file_object.save()
                    claim.files.add(file_object)
                claim.save()
