from apps.user.models import User, WechatAccount
from rest_framework import authentication


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        xuetangx_source = request.META.get("HTTP_X_XUETANGXSOURCE")
        if xuetangx_source == "mini-program":
            mini_program_session_key = request.META.get("HTTP_X_MINIPROGRAMSESSION")
            user = WechatAccount.get_user(mini_program_session_key=mini_program_session_key)
            return user, None
        return None
