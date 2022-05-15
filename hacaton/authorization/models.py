from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from datetime import datetime
from hacaton import settings
import uuid


class UserManager(BaseUserManager):
    def create_user(self, username, password):
        if username is None:
            raise TypeError('Users must have a username.')
        if password is None:
            raise TypeError('Users must have a password.')

        user = self.model(username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


class TokenManager(models.Manager):
    def create_session(self, user, refresh):
        kwargs = dict()
        kwargs['user'] = user
        kwargs['refresh_token'] = refresh
        return self.create(**kwargs)

    def delete_current_session(self, request):
        return self.filter(access_token=request.auth).delete()

    def update_tokens(self, access_token, refresh_token):
        session = self.get(access_token=access_token, refresh_token=refresh_token)
        session.access_token = self._get_uuid()
        session.refresh_token = self._get_uuid()
        session.save()

    def _get_uuid(self):
        return str(uuid.uuid4())


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=1024, unique=True, null=False)
    refresh_destroy_time = models.DateTimeField(default=datetime.now()+settings.REFRESH_TOKEN_LIFETIME, null=False)

    objects = TokenManager()

    def refresh_is_valid(self):
        return datetime.now() < self.refresh_destroy_time


class RecallToken(models.Model):
    recalled_token_hash = models.CharField(max_length=1024, null=False)
    racalled_token_destroy_time = models.DateTimeField(null=False)
