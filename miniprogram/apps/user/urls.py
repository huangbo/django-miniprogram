from django.conf.urls import url
from apps.user.views.user_views import UsersView
from apps.user.views.auth_views import UserView, UserAccessView
from apps.user.views.auth_views import create_wechat_user


urlpatterns = [
    url(r'^users/?$', UsersView.as_view(), name='users'),
    # sign in
    url(r'^$', UserView.as_view(), name='user'),
    # sign up
    url(r'^access/?$', UserAccessView.as_view(), name='access'),
    # wechat user sign in
    url(r'^wechat-user/?$', create_wechat_user, name='wechat-user'),

]