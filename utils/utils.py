from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, Http404):
            raise Http404()
        elif isinstance(exc, PermissionDenied):
            raise PermissionDenied()
        else:
            raise exc

    return response
