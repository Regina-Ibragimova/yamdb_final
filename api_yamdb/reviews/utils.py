from django.utils import timezone
from rest_framework.exceptions import ValidationError


def current_year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            '%(value)s is not a correcrt year!',
            params={'value': value},
        )
