# -*- coding: utf-8 -*-
import uuid
import requests
from constants import sms_c
from libs.utils.treasures import str_byte_cmp
from libs.cache.redis_cache import RedisCache


class YunPianSMS(object):
    # todo limit sms send server

    def __init__(self):
        self.apikey = sms_c.YUNPIAN_API_KEY

    @staticmethod
    def sms_code():
        code = str(uuid.uuid4().int)[:sms_c.VALIDATE_LENGTH]
        return code

    @staticmethod
    def redis_sms_code(mobile, code):
        redis_cache = RedisCache()
        redis_cache.redis_set_key("{}{}".format(sms_c.SMS_REDIS_PREFIX, mobile), code, sms_c.VALIDATE_TIME)

    def sms_send(self, mobile, content, timeout=3, verify=False):
        data = {
            "apikey": self.apikey,
            "mobile": mobile,
            "text": content,
        }
        resp = requests.post(
            "http://yunpian.com/v1/sms/send.json",
            data,
            timeout=timeout,
            verify=verify
        )
        return resp.content

    def check_verification_code(self, mobile, code):
        redis_cache = RedisCache()
        sms_code = redis_cache.redis_get_key("{}{}".format(sms_c.SMS_REDIS_PREFIX, mobile))
        print(sms_code)
        print(code)
        return str_byte_cmp(sms_code, code)

    def verification_code(self, mobile):
        code = self.sms_code()
        content = u'您的验证码是{}。如非本人操作，请忽略本短信。【学堂在线】' .format(code)
        self.redis_sms_code(mobile, code)
        return self.sms_send(mobile, content)
