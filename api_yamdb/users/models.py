from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from users import constants
from users.validations import validate_email


class UserCreatePatch(UserManager):
    def create_user(self, username, email, password, **extra_fields):
        username = validate_email(email, username)
        return super().create_user(
            username,
            email=email,
            password=password,
            **extra_fields
        )

    def create_superuser(
        self,
        username,
        email,
        password,
        role=constants.ADMIN,
        **extra_fields
    ):
        return super().create_superuser(
            username,
            email,
            password,
            role=constants.ADMIN,
            **extra_fields
        )


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email_address',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        max_length=150,
        choices=constants.ROLE_CHOICES,
        default=constants.USER,
        verbose_name='role_user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    objects = UserCreatePatch()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_email'
            ),
            models.CheckConstraint(
                name='me_no_create_user',
                check=~models.Q(username='me')
            )
        ]

    @property
    def is_admin(self):
        return (
            self.is_superuser
            or self.role == constants.ROLE_CHOICES[2][0]
        )

    @property
    def is_moderator(self):
        return self.role == constants.ROLE_CHOICES[1][0]
