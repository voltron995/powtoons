from rest_framework import permissions
from django.shortcuts import get_object_or_404
from apps.powtoons.models import Powtoon

class BaseNoObjectPermission(permissions.BasePermission):
    """ Base class for all permission classes, where permissions are determined
        by view kwargs (such as 'powtoon_id' etc.)
    """

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class IsOwnerOrReadOnly(BaseNoObjectPermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed if powtoon is shared with current user,
        # or current user is admin, or can see all powtoons
        # so we'll allow GET, HEAD or OPTIONS requests.
        powtoon = get_object_or_404(Powtoon, pk=view.kwargs.get('powtoon_id'))
        is_admin = request.user.groups.filter(name='admin').exists()
        can_see_all_powtoons = request.user.has_perm('can_get_all_powtoons')
        is_in_shared_users = request.user in powtoon.shared_with.all()
        if request.method in permissions.SAFE_METHODS \
            and (is_admin or can_see_all_powtoons or is_in_shared_users):
            return True
        elif request.method not in permissions.SAFE_METHODS and is_admin:
            return True

        # Write permissions are only allowed to the owner .
        return powtoon.owner == request.user

class IsAllowedToShare(BaseNoObjectPermission):
    """
    Custom permission to only allow owners of an object to shere it in case they
        have proper permission.
    """

    def has_permission(self, request, view):

        is_admin = request.user.groups.filter(name='admin').exists()
        can_share_powtoons = request.user.has_perm('can_share_powtoons')
        if request.method in ["PUT", "PATCH"] and request.data.get('shared_with'):
            if can_share_powtoons or is_admin:
                return True
            return False
        return True
