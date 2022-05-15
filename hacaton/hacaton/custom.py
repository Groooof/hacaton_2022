from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler
import rest_framework.exceptions


class CustomJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = '' if data is None else data
        err_key = '_err'
        is_err = err_key in data

        response_data = {'success': not is_err,
                         'err': data[err_key] if is_err else '',
                         'data': data if not is_err else ''}

        response = super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)
        return response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    err_key = '_err'
    err_value = exc.detail

    if isinstance(exc, rest_framework.exceptions.ValidationError):
        err_value = 'VALIDATION_ERROR'
    elif isinstance(exc,
                    (rest_framework.exceptions.AuthenticationFailed,
                     rest_framework.exceptions.NotAuthenticated,
                     rest_framework.exceptions.PermissionDenied)):
        err_value = 'PERMISSION_DENIED'

    response.data = {err_key: err_value}

    return response
