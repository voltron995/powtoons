from django.contrib.auth.models import Permission
from django.contrib import admin

from apps.powtoons.models import Powtoon
admin.site.register(Permission)
admin.site.register(Powtoon)
