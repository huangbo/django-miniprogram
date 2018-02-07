import time
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, AnonymousUser
from django.contrib.auth import login, logout
from django.utils import timezone
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from libs.cache.redis_cache import RedisCache
from constants import user_c

# Create your models here.


class AbstractUser(AbstractBaseUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = True

    def clean(self):
        super(AbstractUser, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return ""

    def get_short_name(self):
        "Returns the short name for the user."
        return ""

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        pass


class User(AbstractUser, TimeStampedModel):

    name = models.CharField(max_length=150, default="", blank=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, choices=user_c.GENDER_CHOICE, default=user_c.GENDER_UNKNOWN, blank=True)
    avatar_url = models.URLField(default="", blank=True)
    edu = models.CharField(max_length=10, choices=user_c.EDU_CHOICE, default=user_c.EDU_OTHER, blank=True)
    career = models.CharField(max_length=150, default="", blank=True)
    married = models.CharField(max_length=10, choices=user_c.MARRIED_CHOICE, default=user_c.MARRIED_UNKNOWN, blank=True)

    mobile = models.CharField(max_length=12, null=True, unique=True)  # unique and empty-string
    mobile_verified = models.BooleanField(default=False)
    email = models.CharField(max_length=80, null=True, unique=True)  # unique and empty-string
    email_verified = models.BooleanField(default=False)
    identity = models.CharField(max_length=80, null=True, unique=True)  # unique and empty-string
    identity_verified = models.BooleanField(default=False)

    subscribed = models.BooleanField(default=False, blank=True)
    channel = models.CharField(max_length=150, default="", blank=True)

    last_login = models.DateTimeField(null=True)
    status = models.IntegerField(choices=user_c.STATUS_CHOICE, default=user_c.STATUS_VALID, blank=True)

    @property
    def wechat_openid(self):
        return self.wechat_account.openid

    @classmethod
    def user_login(cls, request, login_user):
        # for session auth
        if isinstance(login_user, cls):
            login(request, login_user)
            request.session.set_expiry(0)
        else:
            return False
        return True

    @classmethod
    def user_logout(cls, request):
        # for session auth
        logout(request)
        return True

    @classmethod
    def get_user(cls, mini_program_session_key=""):
        if mini_program_session_key:
            redis_cache = RedisCache(settings.REDIS_DB_SESSION)
            mini_program_session = redis_cache.redis_m_get_hash(mini_program_session_key)
            unionid = mini_program_session.get(b"unionid", '')
            openid = mini_program_session.get(b"openid", '')
            try:
                return WechatAccount.objects.get(unionid=unionid, openid=openid).user
            except WechatAccount.DoesNotExist as e:
                return AnonymousUser()
        return AnonymousUser()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        app_label = "user"


class WechatAccount(TimeStampedModel):
    openid = models.CharField(max_length=190, primary_key=True)
    unionid = models.CharField(max_length=255, default='')
    session_key = models.CharField(max_length=255, default='')

    user = models.OneToOneField(User, related_name='wechat_account')

    @classmethod
    def create_wechat_user(cls, openid, unionid, session_key):
        if cls.objects.filter(unionid=unionid, openid=openid).exists():
            return True
        # todo transaction
        new_user = User(username=str(int(time.time())), last_login=timezone.now())
        new_user.save()
        new_wechat = cls(openid=openid, unionid=unionid, session_key=session_key, user=new_user)
        new_wechat.save()

    @classmethod
    def mini_program_login(cls, mini_program_session_key, session_info):
        # for mini-program login
        redis_cache = RedisCache(settings.REDIS_DB_SESSION)
        redis_cache.redis_m_add_to_hash(mini_program_session_key, session_info)

    class Meta:
        app_label = "user"


class WeiboAccount(TimeStampedModel):
    openid = models.CharField(max_length=190, primary_key=True)
    user = models.OneToOneField(User, related_name='weibo_account')

    class Meta:
        app_label = "user"


class QQAccount(TimeStampedModel):
    openid = models.CharField(max_length=190, primary_key=True)
    user = models.OneToOneField(User, related_name='qq_account')

    class Meta:
        app_label = "user"
