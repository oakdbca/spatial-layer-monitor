"""Thermal Image Processing Django Application Permissions."""

# Third-Party
import django
from django.conf import settings
from django.contrib.auth import models
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from rest_framework import permissions, request, viewsets
import logging

# Configure logging
logger = logging.getLogger(__name__)


# Typing
from typing import Union
from typing import Any

class IsInOfficersGroup(permissions.BasePermission):
    """Permissions for the a user in the Administrators group."""

    def has_permission(  # type: ignore
        self,
        request: request.Request,
        view: viewsets.GenericViewSet,
    ) -> bool:
        return is_officer(request.user)



def is_officer(user: Union[models.User, models.AnonymousUser]) -> bool:
    """Checks whether a user is an Officer.

    Args:
        user (Union[models.User, models.AnonymousUser]): User to be checked.

    Returns:
        bool: Whether the user is in the Officer group.
    """
    # Check and Return
    group = django.contrib.auth.models.Group.objects.filter(name=settings.GROUP_OFFICERS).first()
    return (
        not isinstance(user, models.AnonymousUser)  # Must be logged in
        and group is not None
        and user.groups.filter(id=group.id).exists()  # Must be in group
    )


class IsAdministratorMixin(AccessMixin):
    """ if user is not administrator, decline permission """

    def dispatch(self, request, *args, **kwargs):
        """
        if user is authenticated and administrator
            we are good. otherwise permission denied
        """
        if request.user.is_authenticated and is_officer(request.user):
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied('Permission denied')  # decline permission