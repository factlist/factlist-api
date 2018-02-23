from django.contrib import admin

from .models import *

admin.site.register(Claim)
admin.site.register(ClaimLink)
admin.site.register(Evidence)
admin.site.register(EvidenceLink)


# Register your models here.
