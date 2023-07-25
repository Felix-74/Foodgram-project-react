from django.db import models
from django.db.models import UniqueConstraint

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''
    Модель юзера
    https://docs.djangoproject.com/en/4.2/ref/contrib/auth/
    '''

    username = models.CharField('username', max_length=254)
    last_name = models.CharField('Фамилия', max_length=254, blank=False)
    first_name = models.CharField('Имя', max_length=254, blank=False)
    email = models.EmailField('E-mail', max_length=254, unique=True, blank=False)

    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')
    USERNAME_FIELD = 'email'


class Subscription(models.Model):
    '''
    Модель подписки
    '''
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

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('user', 'author'),
                name='user_author_unique'
            )
        ]
