from django.core.exceptions import PermissionDenied
from .models import Estate

def user_is_member_of_estate(function):
    def wrap(request, *args, **kwargs):
        estate = Estate.objects.get(pk=kwargs['estate_id'])
        users = estate.users.all()
        if request.user in users:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap