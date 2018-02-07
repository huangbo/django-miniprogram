from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.user.models import User, WechatAccount, MobileAccount
from libs.wechat.client import MiniProgram
from libs.sms.sms_server import YunPianSMS
from constants import error_c, user_c


# mini-program sign up
class MiniProgramUserAccessView(GenericAPIView):
    def post(self, request):
        js_code = request.data.get("js_code", "")
        mini_program = MiniProgram()
        session_info = mini_program.exchange_code_for_session_key(js_code=js_code)
        print(session_info)

        session_key = session_info.get("session_key", "")
        openid = session_info.get("openid", "")
        unionid = session_info.get("unionid", "")
        if session_key and openid:
            WechatAccount.create_wechat_user(openid=openid, unionid=unionid, session_key=session_key)
            mini_program_session_key = mini_program.session_key()
            WechatAccount.mini_program_login(mini_program_session_key, session_info)
            return Response({"retCode": error_c.ERR_SUCCESS[0], "retMsg": error_c.ERR_SUCCESS[1],
                             "mini_program_session_key": mini_program_session_key}, status.HTTP_200_OK)
        else:
            return Response({"retCode": error_c.ERR_SUCCESS[0], "retMsg": error_c.ERR_SUCCESS[1]}, status.HTTP_200_OK)


# mobile sign up
class MobileUserAccessView(GenericAPIView):
    def post(self, request):
        response = Response({"retCode": error_c.ERR_SUCCESS[0], "retMsg": error_c.ERR_SUCCESS[1]}, status.HTTP_200_OK)
        mobile = request.POST.get("mobile", "")
        code = request.POST.get("code", "")
        verify_ret = YunPianSMS().check_verification_code(mobile, code)
        login_user = MobileAccount.create_mobile_user(mobile)
        if verify_ret and login_user:
            User.user_login(request, login_user)
            response.set_cookie(user_c.USER_SIGN_UP_WAY_KEY, user_c.USER_SIGN_UP_WAY_MOBILE)
            return response
        return Response({"retCode": error_c.VERIFY_ERROR_SMS[0], "retMsg": error_c.VERIFY_ERROR_SMS[1]},
                        status.HTTP_400_BAD_REQUEST)


# web user sign up
class WebUserView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        login_user = authenticate(request, username=username, password=password)
        User.user_login(request, login_user)
        return Response({"retCode": "success"}, status.HTTP_200_OK)

    def delete(self, request):
        User.user_logout(request)
        return Response({"retCode": "success"}, status.HTTP_200_OK)


# account binder
class AccountBinderView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request):
        user = request.user
        binder = request.POST.get("binder", "")

        if binder == "mobile":
            mobile = request.POST.get("mobile", "")
            code = request.POST.get("code", "")
            verify_ret = YunPianSMS().check_verification_code(mobile, code)
            if verify_ret and MobileAccount.mobile_binder(user, mobile):
                return Response({"retCode": error_c.ERR_SUCCESS[0], "retMsg": error_c.ERR_SUCCESS[1]},
                                status.HTTP_200_OK)
        else:
            pass
        return Response({"retCode": error_c.ERR_FAIL[0], "retMsg": error_c.ERR_FAIL[1]},
                        status.HTTP_400_BAD_REQUEST)


class MiniProgramUserInfoView(GenericAPIView):
    def get(self, request):
        encrypted_data = request.GET.get("encryptedData", "")
        iv = request.GET.get("iv", "")

        session_key = "VYZn4ndtEpOSGMEydEFjzQ=="

        crypt = MiniProgram()
        user_info = crypt.decrypt(encrypted_data, iv, session_key)
        print(user_info)
        return Response({"retCode": "success"}, status.HTTP_200_OK)