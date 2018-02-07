from constants import user_c
from apps.user.models import User
from django.utils.deprecation import MiddlewareMixin


class CsrfTokenSkip(MiddlewareMixin):
    """
    Middleware catch user last active time
    """
    def process_request(self, request):
            setattr(request, '_dont_enforce_csrf_checks', True)
