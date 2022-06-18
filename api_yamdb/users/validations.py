import re

from rest_framework import serializers
from users import constants
from users.constants import EXTRA_USER, MESSEGE_ERROR_EXTRA_USER


def validate_email(email, username):
    if not email:
        raise ValueError(
            'Fill in the "email" field'
        )
    if username == EXTRA_USER:
        raise ValueError(
            MESSEGE_ERROR_EXTRA_USER
        )
    if username is None:
        username = email.split('@')[0]
    if re.match(r"^[a-z._]+$", username):
        raise ValueError(
            'It is allowed to use only letters, numbers and @/./+/-/_.'
        )
    return username


def validate_username(self, value):
    if value == constants.EXTRA_USER:
        raise serializers.ValidationError(
            constants.MESSEGE_ERROR_EXTRA_USER
        )
    return value
