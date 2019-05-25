from functools import wraps
from django.conf import settings
from django.shortcuts import redirect


def already_logged_in(func):
    @wraps(func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return func(request, *args, **kwargs)
    return wrapper_func
