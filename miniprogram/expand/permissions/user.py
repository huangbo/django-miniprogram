from rest_framework.permissions import BasePermission
from constants import user_c

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class CMSManagerPermission(BasePermission):
    """
    The request is authenticated as a cms admin user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in [user_c.ROLE_MANAGER, user_c.ROLE_ADMIN]
        )