from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """User model."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    username = models.CharField(
        'username',
        unique=True,
        max_length=150,
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+'
            )
        ]
    )
    email = models.EmailField(
        'email address',
        unique=True,
        max_length=254,
        blank=False,
    )
    first_name = models.CharField(
        'first name',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'last name',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        choices=USER_ROLES_CHOICES,
        default='user',
        max_length=13,
        blank=True,
    )
    confirmation_code = models.CharField(
        null=True,
        max_length=100
    )

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_name'
            ),
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_admin_or_superuser(self):
        return self.role == User.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_user(self):
        return self.role == User.USER
