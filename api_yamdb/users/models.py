from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODER = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, USER),
    (MODER, MODER),
    (ADMIN, ADMIN)
)


class User(AbstractUser):
    password = models.CharField(max_length=128, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(max_length=5, choices=ROLES,
                            default=USER, blank=True)

    class Meta:
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODER

    @property
    def is_user(self):
        return self.role == USER
