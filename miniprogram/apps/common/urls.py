from django.conf.urls import url
from apps.common.views.sms_views import SMSCodeView

urlpatterns = [
    url(r'^sms_code/?$', SMSCodeView.as_view(), name='sms-code'),
]