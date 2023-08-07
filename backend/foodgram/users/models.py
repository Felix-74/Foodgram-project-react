from django.db import models
from django.db.models import UniqueConstraint

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Модель юзера
    https://docs.djangoproject.com/en/4.2/topics/auth/customizing/
    """

    username = models.CharField('username', max_length=254)
    last_name = models.CharField('Фамилия', max_length=254, blank=False)
    first_name = models.CharField('Имя', max_length=254, blank=False)
    email = models.EmailField('E-mail', max_length=254, unique=True,
                              blank=False)

    REQUIRED_FIELDS = ('username', 'last_name', 'first_name')
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """
    Модель подписки
    """
    user = models.ForeignKey(
        User,
        verbose_name='Фолловер',
        related_name='follow',
        on_delete=models.CASCADE,

    )
    author = models.ForeignKey(
        User,
        verbose_name='Юзер',
        related_name='user',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user} + {self.author}'

    class Meta:
        ordering = ('-author_id', )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                fields=('user', 'author'),
                name='unique_constraint_user_author'
            )
        ]
