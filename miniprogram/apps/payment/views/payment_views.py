from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from libs.wechat.pay import WXAppPay
from libs.utils.treasures import get_request_ip
from rest_framework.permissions import IsAuthenticated


class PaymentView(CreateAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        model_name = request.data.get("model_name", "")
        app_label = request.data.get("app_label", "")
        instance = request.data.get("instance", 0)
        try:
            PaymentModel = apps.get_model(app_label=app_label, model_name=model_name)
            instance = PaymentModel.objects.get(pk=instance)
        except (LookupError, ObjectDoesNotExist) as e:
            return Response({"retCode": "fail", "retMsg": str(e)}, status.HTTP_400_BAD_REQUEST)

        mini_program_pay = WXAppPay()
        unifiedorder = mini_program_pay.unifiedorder(body=instance.payment_body,
                                                     out_trade_no=mini_program_pay.generate_trade_no(),
                                                     total_fee=instance.discount_price,
                                                     openid=request.user.wechat_openid,
                                                     detail=instance.payment_detail,
                                                     attach=instance.payment_attach,
                                                     spbill_create_ip=get_request_ip(request))
        print(unifiedorder)

        return Response({"retCode": "success", "unifiedorder": unifiedorder}, status.HTTP_200_OK)
