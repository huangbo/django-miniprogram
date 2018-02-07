from django.conf.urls import url
from apps.user.views import UsersView


urlpatterns = [
    url(r'^users/?$', UsersView.as_view(), name='users'),
]