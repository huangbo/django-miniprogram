from django.db import models
from django_extensions.db.models import TimeStampedModel
# Create your models here.


class User(TimeStampedModel):
    # GENDER
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_UNKNOWN = "unknown"
    GENDER_CHOICE = (
        (GENDER_MALE, "男"),
        (GENDER_FEMALE, "女"),
        (GENDER_UNKNOWN, "未知"),
    )

    # EDU
    EDU_JUNIOR_COLLEGE = "junior"
    EDU_UNDERGRADUATE = "undergraduate"
    EDU_MASTER = "master"
    EDU_DOCTOR = "doctor"
    EDU_OTHER = "other"
    EDU_CHOICE = (
        (EDU_JUNIOR_COLLEGE, "专科"),
        (EDU_UNDERGRADUATE, "本科"),
        (EDU_MASTER, "硕士"),
        (EDU_DOCTOR, "博士"),
        (EDU_OTHER, "其他"),
    )

    # MARRIED
    MARRIED = "yes"
    MARRIED_NO = "no"
    MARRIED_UNKNOWN = "unknown"
    MARRIED_CHOICE = (
        (MARRIED, "已婚"),
        (MARRIED_NO, "未婚"),
        (MARRIED_UNKNOWN, "未知"),
    )

    # STATUS
    STATUS_VALIDATED = 1
    STATUS_INVALIDATED = 0
    STATUS_CHOICE = (
        (STATUS_VALIDATED, "validated"),
        (MARRIED_NO, "invalidated"),
    )

    name = models.CharField(max_length=150, default="", blank=True)
    display_name = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, default=GENDER_UNKNOWN, blank=True)
    avatar_url = models.URLField(default="", blank=True)
    edu = models.CharField(max_length=10, choices=EDU_CHOICE, default=EDU_OTHER, blank=True)
    career = models.CharField(max_length=150, default="", blank=True)
    married = models.CharField(max_length=10, choices=MARRIED_CHOICE, default=MARRIED_UNKNOWN, blank=True)

    mobile = models.CharField(max_length=12, null=True, unique=True)  # unique and empty-string
    mobile_verified = models.BooleanField(default=False)
    email = models.CharField(max_length=80, null=True, unique=True)  # unique and empty-string
    email_verified = models.BooleanField(default=False)
    identity = models.CharField(max_length=80, null=True, unique=True)  # unique and empty-string
    identity_verified = models.BooleanField(default=False)

    subscribed = models.BooleanField(default=False, blank=True)
    channel = models.CharField(max_length=150, default="", blank=True)

    last_login = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_CHOICE, default=STATUS_VALIDATED, blank=True)

    class Meta:
        app_label = "user"


class WechatAccount(models.Model):
    wechat_open_id = models.CharField(max_length=190, primary_key=True)
    wechat_unionid = models.CharField(max_length=255, default=' ')
    user = models.OneToOneField(User, related_name='wechat_account')

    class Meta:
        app_label = "user"


class WeiboAccount(models.Model):
    weibo_open_id = models.CharField(max_length=190, primary_key=True)
    user = models.OneToOneField(User, related_name='weibo_account')

    class Meta:
        app_label = "user"


class QQAccount(models.Model):
    weibo_open_id = models.CharField(max_length=190, primary_key=True)
    user = models.OneToOneField(User, related_name='qq_account')

    class Meta:
        app_label = "user"
