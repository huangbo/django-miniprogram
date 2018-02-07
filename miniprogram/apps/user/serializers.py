import logging
from rest_framework import serializers
from apps.user.models import User

log = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'display_name', 'password', 'last_login', 'gender')
