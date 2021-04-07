"""Decorators for Views"""
from django.core.exceptions import PermissionDenied

from .models import Estate


def user_is_member_of_estate(function):
    """Decorator checking if user is member of estate"""

    def wrap(request, *args, **kwargs):
        """Wrapper for user_is_member_of_estate"""
        estate = Estate.objects.get(pk=kwargs['estate_id'])
        users = estate.users.all()
        if request.user in users:
            return function(request, *args, **kwargs)

        raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
