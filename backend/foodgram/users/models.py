from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models

from .validators import not_me_username_validation


class User(AbstractUser):

    USER_ROLE = 'user'
    ADMIN_ROLE = 'admin'

    ACCESS_ROLES = (
        (USER_ROLE, 'user'),
        (ADMIN_ROLE, 'admin')
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            ASCIIUsernameValidator(),
            not_me_username_validation
        ]
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False
    )
    role = models.CharField(
        max_length=max(
            len(iteration[0]) for iteration in ACCESS_ROLES),
        choices=ACCESS_ROLES,
        default=USER_ROLE,
        blank=False,
        verbose_name='роль'
    )
    password = models.CharField(max_length=128, blank=False)

    @property
    def is_user(self):
        return self.role == self.USER_ROLE

    @property
    def is_admin(self):
        return (self.role == self.ADMIN_ROLE
                or self.is_staff)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            ),
        ]
