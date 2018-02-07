from django.conf.urls import url
from apps.user.views.user_views import UsersView
from apps.user.views.auth_views import UserView, UserAccessView, UserInfoView

urlpatterns = [
    url(r'^users/?$', UsersView.as_view(), name='users'),
    # sign in
    url(r'^$', UserView.as_view(), name='user'),
    # sign up
    url(r'^access/?$', UserAccessView.as_view(), name='access'),
    url(r'^mini-program-user/?$', UserInfoView.as_view(), name='mini-program-user'),
]