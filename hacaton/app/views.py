from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django_hosts.resolvers import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.template.loader import render_to_string
from hacaton import settings
from authorization.views import refresh


class AppAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'app/index.html')
        return redirect(reverse('auth_page', host='empty'))

        # at = request.COOKIES.get('at', None)
        # rt = request.COOKIES.get('rt', None)
        # fp = request.COOKIES.get('fp', None)
        # res = refresh(at, rt, fp)
        # if res is None:
        #     response = redirect(reverse('auth_page', host='empty'))
        #     print(response)
        #     return response
        # print(111111111111111111111111111111111111111111111)
        # new_at, new_rt, new_fp = res
        # response = render(request, 'app/index.html')
        # response.set_cookie('at', new_at, httponly=True, domain='.hacaton.local', path='/',
        #                     max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(), samesite='strict',
        #                     secure=False)
        # response.set_cookie('fp', new_fp, httponly=True, domain='.hacaton.local', path='/',
        #                     max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(), samesite='strict',
        #                     secure=False)
        # response.set_cookie('rt', new_rt, httponly=True, domain='.hacaton.local', path='/',
        #                     max_age=settings.REFRESH_TOKEN_LIFETIME.total_seconds(), samesite='strict',
        #                     secure=False)
        #
        # return response



