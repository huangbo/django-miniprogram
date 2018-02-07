from constants import user_c
from apps.user.models import User
from django.utils.deprecation import MiddlewareMixin


class UserForceLogoutMiddleware(MiddlewareMixin):
    """
    Middleware catch user last active time
    """
    def process_request(self, request):
        if (request.COOKIES.get(user_c.USER_SIGN_UP_WAY_KEY, "") == user_c.USER_SIGN_UP_WAY_MOBILE) and (request.user.is_authenticated()):
            # todo maybe modify
            if not hasattr(request.user, "mobile_account"):
                User.user_logout(request)
        return None
