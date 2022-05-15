from rest_framework import authentication
from rest_framework.serializers import UUIDField
from rest_framework import exceptions as drf_exceptions
from .models import User, Token, RecallToken
from . import exceptions
from . import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request, **kwargs):
        at = request.COOKIES.get('at', None)
        fp = request.COOKIES.get('fp', None)
        if fp is None or at is None:
            print('FP or AT NONE')
            return None
            # raise exceptions.FingerprintRequired

        return self.authenticate_credentials(at, fp)

    def authenticate_credentials(self, token, fp):
        if not jwt.check_at_exp(token):
            print('EXPR')
            return None
            #raise exceptions.ExpiredTokenError

        if not jwt.check_at_sign(token):
            print('SIGN')
            return None
            #raise exceptions.InvalidTokenError

        if not jwt.check_at_fingerprint(token, fp):
            print('FP')
            return None
            #raise exceptions.InvalidTokenError

        token_hash = jwt.gen_sha256(token)
        if RecallToken.objects.filter(recalled_token_hash=token_hash).exists():
            print('BLACKLIST')
            return None
            #raise exceptions.InvalidTokenError

        decoded_token = jwt.decode_jwt(token)
        user_id = decoded_token[1]['user_id']

        user = User.objects.get(pk=user_id)

        return user, token

