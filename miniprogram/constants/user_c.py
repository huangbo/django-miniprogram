# web sign up way

USER_SIGN_UP_WAY_KEY = "sign_up_way"
USER_SIGN_UP_WAY_MOBILE = "mobile"
USER_SIGN_UP_WAY_WEB_CMS = "web-cms"

# user terminal
SOURCE_WECHAT = "wechat"


# gender
GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_UNKNOWN = "unknown"
GENDER_CHOICE = (
    (GENDER_MALE, "男"),
    (GENDER_FEMALE, "女"),
    (GENDER_UNKNOWN, "未知"),
)

# edu
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

# married
MARRIED = "yes"
MARRIED_NO = "no"
MARRIED_UNKNOWN = "unknown"
MARRIED_CHOICE = (
    (MARRIED, "已婚"),
    (MARRIED_NO, "未婚"),
    (MARRIED_UNKNOWN, "未知"),
)

# status
STATUS_VALID = 1
STATUS_INVALID = 0
STATUS_CHOICE = (
    (STATUS_VALID, "valid"),
    (STATUS_INVALID, "invalid"),
)

# role
ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_MANAGER = 2
ROLE_JUDGES = 3
ROLE_CHOICE = (
    (ROLE_USER, "User"),
    (ROLE_ADMIN, "Admin"),
    (ROLE_MANAGER, "Manager"),
    (ROLE_JUDGES, "Judges"),
)
