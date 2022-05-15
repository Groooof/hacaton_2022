from rest_framework.exceptions import APIException
from rest_framework import status


class UserAlreadyExistsError(APIException):
    default_detail = 'USER_EXISTS'
    status_code = status.HTTP_409_CONFLICT


class WrongCredentialsError(APIException):
    default_detail = 'WRONG_CREDENTIALS'
    status_code = status.HTTP_401_UNAUTHORIZED


class AuthorizationError(APIException):
    default_detail = 'PERMISSION_DENIED'
    status_code = status.HTTP_401_UNAUTHORIZED


class ExpiredTokenError(APIException):
    default_detail = 'TOKEN_EXPIRED'
    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidTokenError(APIException):
    default_detail = 'INVALID_TOKEN'
    status_code = status.HTTP_401_UNAUTHORIZED


class DoesNotExistError(APIException):
    default_detail = 'DOES_NOT_EXIST'
    status_code = status.HTTP_404_NOT_FOUND


class FingerprintRequired(APIException):
    default_detail = 'FINGERPRINT_REQUIRED'
    status_code = status.HTTP_401_UNAUTHORIZED



