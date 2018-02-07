from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.user.models import User, WechatAccount
from libs.wechat.client import MiniProgram


# user sign up
class UserAccessView(GenericAPIView):
    def get(self, request):
        js_code = request.GET.get("js_code", "")
        mini_program = MiniProgram()
        session_info = mini_program.exchange_code_for_session_key(js_code=js_code)
        print(session_info)

        session_key = session_info.get("session_key", "")
        openid = session_info.get("openid", "")
        unionid = session_info.get("unionid", "")
        if session_key and openid:
            WechatAccount.create_wechat_user(openid=openid, unionid=unionid, session_key=session_key)
            mini_program_session_key = mini_program.session_key()
            User.mini_program_login(mini_program_session_key, session_info)
            return Response({"retCode": "success", "mini_program_session_key": mini_program_session_key}, status.HTTP_200_OK)
        else:
            return Response({"retCode": "fail"}, status.HTTP_200_OK)


class UserInfoView(GenericAPIView):
    def get(self, request):
        encrypted_data = request.GET.get("encryptedData", "")
        iv = request.GET.get("iv", "")

        session_key = "qxOGREzE++ZY3bUQEv80tQ=="

        crypt = MiniProgram()
        user_info = crypt.decrypt(encrypted_data, iv, session_key)
        print(user_info)
        return Response({"retCode": "success"}, status.HTTP_200_OK)


class UserView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        login_user = authenticate(request, username=username, password=password)
        User.user_login(request, login_user)
        return Response({"retCode": "success"}, status.HTTP_200_OK)

    def delete(self, request):
        User.user_logout(request)
        return Response({"retCode": "success"}, status.HTTP_200_OK)

