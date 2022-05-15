from django.urls import path, include
from . import views

urlpatterns = [
    path(r'', views.AuthPageAPIView.as_view(), name='auth_page'),
    path(r'api/v1/signup', views.RegistrationAPIView.as_view()),
    path(r'api/v1/login', views.LoginAPIView.as_view()),
    # path(r'api/v1/refresh', views.RefreshAPIView.as_view(), name='refresh'),
    # path(r'page1', views.AppAPIView.as_view(), name='app_page'),
]





