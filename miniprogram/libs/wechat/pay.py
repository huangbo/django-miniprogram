import time
import requests
import xmltodict
import hashlib
from constants.wechat_c import USE_MINI_PROGRAM
from libs.wechat.helper import smart_str, smart_unicode
from libs.utils.treasures import generate_32_uuid


class WeixinPay(object):
    TIMEOUT = 5
    WECHAT_PAY_URL = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    NOTIFY_URL = 'http://xuetangx.tunnel.xuetangx.com'

    def __init__(self, use_mini_program=USE_MINI_PROGRAM):
        self.appid = use_mini_program.get("appid", "")
        self.mch_id = use_mini_program.get("mch_id", "")
        self.pay_api_key = use_mini_program.get("pay_api_key", "")
        self.mch_cert = use_mini_program.get("mch_cert", "")
        self.mch_key = use_mini_program.get("mch_key", "")

    @staticmethod
    def generate_trade_no():
        random_number = generate_32_uuid()[:6]
        time_number = str(int(time.time()))[1:]
        return time_number + random_number

    @staticmethod
    def generate_nonce_str():
        return generate_32_uuid()

    @staticmethod
    def generate_sign(sign_string, key=None, sign_type='MD5'):
        if sign_type == 'MD5':
            sign_string += '&key=%s' % str(key)
            return hashlib.md5(sign_string.encode("utf8")).hexdigest().upper()
        return ''

    @staticmethod
    def params_encoding(params):
        new_params = {}
        for k, v in params.items():
            new_params[k] = smart_unicode(v)
        return new_params

    @staticmethod
    def params_filter(params, delimiter='&', charset='utf-8', excludes=['sign', 'sign_type']):
        ks = sorted(params.keys())
        new_params = {}
        sign_string = ''
        if params.get('input_charset', None):
            charset = params['input_charset']
        for k in ks:
            v = params[k]
            k = smart_str(k, charset)
            if k not in excludes and v != '':
                new_params[k] = smart_str(v, charset)
                sign_string += '%s=%s%s' % (k, new_params[k], delimiter)
        sign_string = sign_string[:-1]
        return new_params, sign_string

    @classmethod
    def wxpay_notify_verify(cls, post_data, pay_api_key=None):
        # 验证--签名
        _, sign_string = cls.params_filter(post_data, excludes=['sign'])
        mysign = cls.generate_sign(sign_string, key=pay_api_key)
        if mysign != post_data.get('sign'):
            return False
        return True

    def prepare_request(self, params, sign):
        kwargs = {}
        # 将内容转化为unicode xmltodict 只支持unicode
        new_params = self.params_encoding(params)
        new_params['sign'] = sign
        xml_dict = {'xml': new_params}
        kwargs['data'] = smart_str(xmltodict.unparse(xml_dict)).encode("utf-8")
        if self.mch_cert and self.mch_key:
            kwargs['cert'] = (self.mch_cert, self.mch_key)
        return kwargs

    def make_request(self, method, url, kwargs):
        req = requests.request(method, url, timeout=self.TIMEOUT, **kwargs)
        # xml to dict
        result = xmltodict.parse(req.content)
        print(result)
        # 只需要返回数据
        return result.get('xml')

    # 统一下单
    # https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
    def unifiedorder(self, body='', out_trade_no='', total_fee='', openid='',
                     detail='', attach='', time_start='', time_expire='',
                     goods_tag='', product_id='', limit_pay='', device_info='',
                     fee_type='CNY', spbill_create_ip='',
                     trade_type='JSAPI', notify_url=NOTIFY_URL):

        params = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "nonce_str": self.generate_nonce_str(),
            "body": body,
            "total_fee":total_fee,
            "out_trade_no": out_trade_no,
            "openid": openid,
            "fee_type": fee_type,
            "spbill_create_ip": spbill_create_ip,
            "notify_url": notify_url,
            "trade_type": trade_type,
            "device_info": device_info,
            "detail": detail,
            "attach": attach,
            "time_start": time_start,
            "time_expire": time_expire,
            "goods_tag": goods_tag,
            "product_id": product_id,
            "limit_pay": limit_pay,
        }
        new_params, sign_string = self.params_filter(params)
        sign = self.generate_sign(sign_string, self.pay_api_key)

        kwargs = self.prepare_request(new_params, sign)
        return self.make_request("POST", self.WECHAT_PAY_URL, kwargs)


class WXAppPay(WeixinPay):
    """
    mini-program pay
    """

    MINI_PROGRAM_PAY_URL = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    NOTIFY_URL = 'http://xuetangx.tunnel.xuetangx.com'

    def unifiedorder(self, body='', out_trade_no='', total_fee='', openid='',
                     detail='', attach='', time_start='', time_expire='',
                     goods_tag='', product_id='', limit_pay='', device_info='',
                     fee_type='CNY', spbill_create_ip='',
                     trade_type='JSAPI', notify_url=NOTIFY_URL):

        params = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "nonce_str": self.generate_nonce_str(),
            "body": body,
            "total_fee":total_fee,
            "out_trade_no": out_trade_no,
            "openid": openid,
            "fee_type": fee_type,
            "spbill_create_ip": spbill_create_ip,
            "notify_url": notify_url,
            "trade_type": trade_type,
            "device_info": device_info,
            "detail": detail,
            "attach": attach,
            "time_start": time_start,
            "time_expire": time_expire,
            "goods_tag": goods_tag,
            "product_id": product_id,
            "limit_pay": limit_pay,
        }
        new_params, sign_string = self.params_filter(params)
        sign = self.generate_sign(sign_string, self.pay_api_key)

        kwargs = self.prepare_request(new_params, sign)
        result = self.make_request("POST", self.MINI_PROGRAM_PAY_URL, kwargs)
        unifiedorder = self.generate_unifiedorder(result)

        return unifiedorder

    def generate_unifiedorder(self, result):
        params = {
            'timeStamp': str(int(time.time())),
            'nonceStr': result.get('nonce_str'),
            'signType': 'MD5',
            'package': 'prepay_id=' + result.get('prepay_id', ''),
            'appId': self.appid
        }
        new_params, sign_string = self.params_filter(params)
        sign = self.generate_sign(sign_string, key=self.pay_api_key)
        params['sign'] = sign
        params["return_code"] = result.get('return_code')
        params["return_msg"] = result.get('return_msg')
        return params
