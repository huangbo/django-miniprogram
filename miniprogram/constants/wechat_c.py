from django.conf import settings
# wechat info

mini_program_online = {
    "appid": "****",
    "app_secret": "****",
    "mch_id": "****",
    "pay_api_key": "****"
}

mini_program_develop = {
    "appid": "****",
    "app_secret": "****",
    "mch_id": "****",
    "pay_api_key": "****"

}

USE_MINI_PROGRAM = mini_program_develop if settings.DEBUG else mini_program_online
