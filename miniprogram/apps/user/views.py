from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import filters, status

from apps.user.serializers import UserSerializer
from apps.user.models import User
from libs.cache.redis_cache import RedisCache


class UsersView(ListCreateAPIView):
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        redis_cache = RedisCache()
        redis_cache.redis_set_key("set_key", 100)
        print(redis_cache.redis_get_key("set_key"))
        return super(UsersView, self).get(request, *args, **kwargs)
