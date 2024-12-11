from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

# THIS MIDDLEWARE IS USING LOCMEMCACHE BY DEFAULT. IF NO CACHE MECHANISM IS PROVIDED IN SETTINGS, LOCMEMCACHE WILL BE USED
# DO NOT USE LOCMEMCACHE IN PRODUCTION.


class IPLockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        username = request.POST.get('username')  # Assuming username is submitted via POST
        if ip:
            key_ip = f'failed_login_attempts_{ip}'
            attempts_ip = cache.get(key_ip, 0)
            if attempts_ip >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
                # return HttpResponseForbidden("Your IP has been temporarily locked due to multiple failed login attempts.")
                raise PermissionDenied()
            # Check user attempts
            if username:
                key_user = f'failed_login_attempts_{username}'
                attempts_user = cache.get(key_user, 0)
                if attempts_user >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
                    # return HttpResponseForbidden("Your account has been temporarily locked due to multiple failed login attempts.")
                    raise PermissionDenied()
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip