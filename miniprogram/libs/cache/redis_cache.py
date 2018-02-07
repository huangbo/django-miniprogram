from functools import wraps
from django_redis import get_redis_connection
from constants import cache_c


# in seconds key being hit, update ttl
def redis_expire(fun):
    @wraps(fun)
    def _decorator(self, key, *args, **kwargs):
        res = fun(self, key, *args, **kwargs)
        self.raw_redis_connection.expire(key, cache_c.CACHE_EXPIRE_TIMEOUT)
        return res

    return _decorator


class RedisCache(object):
    _instance = {}

    def __new__(cls, alias="default", *args, **kwargs):
        if not hasattr(cls._instance, alias):
            instance = super(RedisCache, cls).__new__(cls)
            instance.raw_redis_connection = get_redis_connection(alias)
            cls._instance[alias] = instance

        return cls._instance[alias]

    # redis base wrap
    def redis_key_exists(self, key):
        return self.raw_redis_connection.exists(key)

    @redis_expire
    def redis_get_key(self, key):
        return self.raw_redis_connection.get(key)

    @redis_expire
    def redis_set_key(self, key, value):
        return self.raw_redis_connection.set(key, value)

    # redis set wrap
    @redis_expire
    def redis_get_set(self, key):
        return self.raw_redis_connection.smembers(key)

    @redis_expire
    def redis_add_to_set(self, key, values):
        if isinstance(values, list):
            self.raw_redis_connection.sadd(key, *values)
        else:
            self.raw_redis_connection.sadd(key, values)

    @redis_expire
    def redis_remove_from_set(self, key, values):
        if isinstance(values, list):
            self.raw_redis_connection.srem(key, 0, *values)
        else:
            self.raw_redis_connection.srem(key, 0, values)

    # redis sorted set
    @redis_expire
    def redis_add_to_sorted_set(self, key, name, value):
        self.raw_redis_connection.zadd(key, value, name)

    @redis_expire
    def redis_get_sorted_set(self, key, start, end):
        return self.raw_redis_connection.zrevrange(key, start, end)
