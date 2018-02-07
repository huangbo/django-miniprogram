from django.conf.urls import url
from apps.user.views.user_views import UsersView
from apps.user.views.auth_views import WebUserView, MiniProgramUserAccessView, MiniProgramUserInfoView, \
    MobileUserAccessView, AccountBinderView

urlpatterns = [
    url(r'^users/?$', UsersView.as_view(), name='users'),
    url(r'^web-user/?$', WebUserView.as_view(), name='web-user'),
    # mini program sign up
    url(r'^mini-program-access/?$', MiniProgramUserAccessView.as_view(), name='mini-program-access'),
    url(r'^mini-program-user/?$', MiniProgramUserInfoView.as_view(), name='mini-program-user'),
    # mobile user
    url(r'^mobile-user/?$', MobileUserAccessView.as_view(), name='mobile-user'),
    # account
    url(r'^account-binder/?$', AccountBinderView.as_view(), name='account-binder'),
]