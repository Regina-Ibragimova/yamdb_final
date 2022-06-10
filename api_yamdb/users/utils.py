from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from api_yamdb.settings import ADMIN_EMAIL_ADDRESS  # isort:skip
from users.models import User  # isort:skip


def sent_confirmation_code(username):
    user = get_object_or_404(User, username=username)
    user.password = User.objects.make_random_password()
    token = default_token_generator.make_token(user)
    send_mail(
        'your confirmation code',
        token,
        ADMIN_EMAIL_ADDRESS,
        [user.email, ],
        fail_silently=False,
    )
