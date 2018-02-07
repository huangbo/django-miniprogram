from django.conf.urls import url
from apps.payment.views.payment_views import PaymentView

urlpatterns = [
    url(r'', PaymentView.as_view(), name='mini-program-payment'),
]