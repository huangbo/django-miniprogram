from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from libs.sms.sms_server import YunPianSMS
from constants import error_c


class SMSCodeView(GenericAPIView):
    def get(self, request):
        mobile = request.GET.get("mobile")
        # todo mobile verify
        if mobile:
            YunPianSMS().verification_code(mobile)
            return Response({"retCode": error_c.ERR_SUCCESS[0], "retMsg": error_c.ERR_SUCCESS[1]},
                            status.HTTP_200_OK)
        return Response({"retCode": error_c.ERR_FAIL[0], "retMsg": error_c.ERR_FAIL[1]},
                        status.HTTP_400_BAD_REQUEST)
