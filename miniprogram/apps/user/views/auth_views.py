from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.user.models import User
from constants import user_c


def create_wechat_user(request):
    wechat_user = User(username="", password="")
    wechat_user.save()
    User.user_login(request, wechat_user)


# user sign in
class UserView(APIView):
    def post(self, request, *args, **kwargs):
        source = request.POST.get("source")
        if source == user_c.SOURCE_WECHAT:
            redirect(reverse("api:user:wechat-user"))
        else:
            pass


# user sign up
class UserAccessView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        login_user = authenticate(request, username=username, password=password)
        User.user_login(request, login_user)
        return Response({"retCode": "success"}, status.HTTP_200_OK)

    def delete(self, request):
        User.user_logout(request)
        return Response({"retCode": "success"}, status.HTTP_200_OK)

