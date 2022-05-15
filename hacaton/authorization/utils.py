from .models import User
from .exceptions import WrongCredentialsError


def authenticate(username, password):
    try:
        user = User.objects.get(username=username)
    except:
            raise WrongCredentialsError
    if not user.check_password(password):
        raise WrongCredentialsError
    return user

