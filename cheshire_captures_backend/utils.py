from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler to raise Django-specific exceptions
    when the DRF exception handler returns None.
    """
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, Http404):
            raise Http404("The requested resource was not found.")
        elif isinstance(exc, PermissionDenied):
            raise PermissionDenied("You do not have permission to access this resource.")
        else:
            raise exc

    return response
