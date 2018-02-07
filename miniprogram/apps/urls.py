from django.conf.urls import include, url


urlpatterns = [
    url(r'^user/', include('apps.user.urls', namespace="user")),
]