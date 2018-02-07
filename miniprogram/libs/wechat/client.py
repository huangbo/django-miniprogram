import requests
import base64
import json
import uuid
from Crypto.Cipher import AES
from six.moves.urllib.parse import urlencode
from constants.wechat_c import USE_MINI_PROGRAM


class MiniProgram(object):
    access_token_url = "https://api.weixin.qq.com/sns/jscode2session"

    def __init__(self, use_mini_program=USE_MINI_PROGRAM):
        self.appid = use_mini_program.get("appid", "")
        self.app_secret = use_mini_program.get("app_secret", "")

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def _data_for_exchange(self, js_code, scope=None):

        iteritems = lambda d, *args, **kwargs: iter(d.items(*args, **kwargs))

        app_params = {
            "appid": self.appid,
            "app_secret": self.app_secret,
        }
        app_params.update(js_code=js_code,
                          secret=self.app_secret,
                          grant_type="authorization_code")

        if scope:
            app_params.update(scope=' '.join(scope))
        str_app_parmas = {}
        for k, v in iteritems(app_params):
            str_app_parmas[k] = str(v).encode('utf-8')
        url_params = urlencode(str_app_parmas)
        return "%s?%s" % (self.access_token_url, url_params)

    def exchange_code_for_session_key(self, js_code=None, scope=None):
        access_token_url = self._data_for_exchange(js_code=js_code, scope=scope)
        try:
            response = requests.get(access_token_url)
        except:
            raise

        parsed_content = json.loads(response.content.decode())
        print(parsed_content)
        return parsed_content

    def decrypt(self, encrypted_data, iv, session_key):
        # base64 decode
        session_key = base64.b64decode(session_key)
        encrypted_data = base64.b64decode(encrypted_data)
        iv = base64.b64decode(iv)

        cipher = AES.new(session_key, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encrypted_data)))

        if decrypted['watermark']['appid'] != self.appid:
            raise Exception('Invalid Buffer')

        return decrypted

    @classmethod
    def session_key(cls):
        session_key = uuid.uuid1()
        return str(session_key).replace("-", "")

