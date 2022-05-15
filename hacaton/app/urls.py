from django.urls import path, include
from . import views

urlpatterns = [
    path(r'', views.AppAPIView.as_view(), name='app_page'),
]





