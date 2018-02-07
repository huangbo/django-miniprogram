from apps.user.models import User
from rest_framework import authentication
from rest_framework import exceptions
from libs.cache.redis_cache import RedisCache


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        xuetangx_source = request.META.get("HTTP_X_XUETANGXSOURCE")
        if xuetangx_source == "mini-program":
            mini_program_session_key = request.META.get("HTTP_X_MINIPROGRAMSESSION")
            redis_cache = RedisCache()
            mini_program_session = redis_cache.redis_m_get_hash(mini_program_session_key)
            print(mini_program_session.get(b"session_key"))
            print(mini_program_session.get(b"openid"))
            try:
                user = User.objects.all()[0]
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('[TokenAuthentication]No such user')
            return user, None
        return None
