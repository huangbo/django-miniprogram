from django.conf.urls import include, url

urlpatterns = [
    url(r'^user/', include('apps.user.urls', namespace="user")),
    url(r'^payment/', include('apps.payment.urls', namespace="payment")),
    url(r'^common/', include('apps.common.urls', namespace="common")),
]
