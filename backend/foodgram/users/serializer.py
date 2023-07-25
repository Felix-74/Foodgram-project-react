from rest_framework.serializers import SerializerMethodField
from users.models import User, Subscription
from djoser.serializers import UserCreateSerializer, UserSerializer as DjoserUserSerializer


class UserSerializer(DjoserUserSerializer):
    '''
    Сериализатор юзера
    https://djoser.readthedocs.io/en/latest/settings.html#serializers
    '''

    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'last_name',
            'email',
            'id',
            'username',
            'first_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        '''
        Узнаем статус подписки
        '''
        if request := self.context.get('request', False) or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()

class UserRegSerializer(UserCreateSerializer):
    '''
    Cериализатор регистрации
    https://djoser.readthedocs.io/en/latest/settings.html#serializers
    '''

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
        )
