from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


class Powtoon(models.Model):
    """ Powtoon main model """

    name = models.CharField(
        verbose_name="name",
        max_length=200,
        null=False, blank=False
    )

    owner = models.ForeignKey(
        verbose_name="user",
        to=User, related_name="powtoon_owner",
        null=True, blank=False, on_delete=models.SET_NULL
    )

    shared_with = models.ManyToManyField(
        verbose_name="shared_with",
        to=User, related_name='powtoon_shared_with',
        null=True, blank=True
    )

    content = JSONField(
        verbose_name="content",
        default=dict
    )

    class Meta:
        verbose_name = "Powtoon"
        verbose_name_plural = "Powtoons"
