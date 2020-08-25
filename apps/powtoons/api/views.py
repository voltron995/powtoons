from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.powtoons.api.permissions import IsAllowedToShare, IsOwnerOrReadOnly
from apps.powtoons.api.serializers import PowtoonCreateUpdateSerializer, PowtoonGetSerializer
from apps.powtoons.models import Powtoon


class PowtoonListCreate(ListCreateAPIView):
    """ Powtoon list/create view
    """

    permission_classes = (
        IsAuthenticated,
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PowtoonGetSerializer
        else:
            return PowtoonCreateUpdateSerializer

    def get_queryset(self):
        current_user = self.request.user
        if current_user.groups.filter(name='admin').exists() or \
        current_user.has_perm('can_get_all_powtoons'):
            return Powtoon.objects.all()
        return Powtoon.objects.filter(Q(owner=current_user) |
                                      Q(shared_with__in=[current_user]))


class PowtoonDetails(RetrieveUpdateDestroyAPIView):
    """ Powtoon get/update/delete
    """

    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
        IsAllowedToShare
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PowtoonGetSerializer
        else:
            return PowtoonCreateUpdateSerializer

    def get_object(self):
        return get_object_or_404(Powtoon, pk=self.kwargs.get('powtoon_id'))
