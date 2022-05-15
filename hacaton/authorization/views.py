import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_hosts.resolvers import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from .utils import authenticate as my_auth
from .models import Token, User
from . import jwt
from hacaton import settings
from . import exceptions


class AuthPageAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('app_page', host='app'))
        return render(request, 'authorization/index.html')

        # at = request.COOKIES.get('at', None)
        # rt = request.COOKIES.get('rt', None)
        # fp = request.COOKIES.get('fp', None)
        # res = refresh(at, rt, fp)
        # if res is None:
        #     return render(request, 'authorization/index.html')
        # new_at, new_rt, new_fp = res
        # response = redirect(reverse('app_page', host='app'))
        # response.set_cookie('at', new_at, httponly=True, domain='.hacaton.local', path='/',
        #                     max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(), samesite='strict', secure=False)
        # response.set_cookie('fp', new_fp, httponly=True, domain='.hacaton.local', path='/',
        #                     max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(), samesite='strict', secure=False)
        # response.set_cookie('rt', new_rt, httponly=True, domain='.hacaton.local', path='/',
        #                     max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(), samesite='strict', secure=False)
        #
        # return response


class RegistrationAPIView(APIView):
    serializer_class = serializers.RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = serializers.UserAuthSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = my_auth(**serializer.validated_data)
        fp = jwt.gen_fingerprint()
        at = jwt.gen_access_token(user.id, fp)
        rt = jwt.gen_refresh_token()
        Token.objects.create_session(user, rt)

        response = Response()
        response.set_cookie('at', at, httponly=True, domain='.hacaton.local', path='/',
                            max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(), samesite='strict', secure=False)
        response.set_cookie('fp', fp, httponly=True, domain='.hacaton.local', path='/',
                            max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(), samesite='strict', secure=False)
        response.set_cookie('rt', rt, httponly=True, domain='.hacaton.local', path='/',
                            max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(), samesite='strict', secure=False)

        return response


def refresh(at, rt, fp):
    if not all((at, rt, fp)):
        print('Not all tokens')
        return None
        raise exceptions.InvalidTokenError

    if jwt.check_at_exp(at):
        print('Not expired')
        return None
        return Response({'32': '234'})

    if not jwt.check_at_sign(at):
        print('Wrong sign')
        return None
        raise exceptions.InvalidTokenError

    if not jwt.check_at_fingerprint(at, fp):
        print('Wrong fingerprint')
        return None
        raise exceptions.InvalidTokenError

    rt_model = Token.objects.get(refresh_token=rt)
    print(rt_model.refresh_destroy_time)
    print(datetime.datetime.now())
    if rt_model.refresh_destroy_time <= datetime.datetime.now():
        print('RT expired')
        return None
        raise exceptions.InvalidTokenError

    _, payload, _ = jwt.decode_jwt(at)
    if payload['user_id'] != rt_model.user.id:
        print('Ne sovpadayut')
        return None
        raise exceptions.InvalidTokenError

    new_fp = jwt.gen_fingerprint()
    new_at = jwt.gen_access_token(payload['user_id'], new_fp)
    new_rt = jwt.gen_refresh_token()

    user = User.objects.get(pk=payload['user_id'])
    Token.objects.create(user=user, refresh_token=new_rt)
    return new_at, new_rt, new_fp


class RefreshAPIView(APIView):
    def post(self, request):
        at = request.COOKIES.get('at', None)
        rt = request.COOKIES.get('rt', None)
        fp = request.COOKIES.get('fp', None)

        response = Response('Refreshed')
        response.set_cookie('at', new_at, httponly=True, domain='.hacaton.local',
                            max_age=settings.ACCESS_TOKEN_LIFETIME.total_seconds(), samesite='strict', secure=False)
        response.set_cookie('fp', new_fp, httponly=True, domain='.hacaton.local',
                            max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(), samesite='strict', secure=False)
        response.set_cookie('rt', new_rt, httponly=True, domain='.hacaton.local',
                            max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(), samesite='strict', secure=False)

        return response


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.delete_current_session(request)
        return Response()


class AppAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response("render_to_string('authorization/app.html', request=request)")


