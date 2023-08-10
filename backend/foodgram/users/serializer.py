from rest_framework.serializers import (SerializerMethodField,
                                        ModelSerializer,
                                        ValidationError)
from rest_framework.validators import UniqueTogetherValidator
from djoser.serializers import (UserCreateSerializer,
                                UserSerializer as DjoserUserSerializer)

from users.models import User, Subscription
from recipes.models import Recipe
from recipes.serializer import ShowFavoriteSerializer
from utils.method_serializer import SerializerMethods

USER_AUTHOR_FIELDS = ('user', 'author')


class UserSerializer(DjoserUserSerializer):
    """
    Сериализатор юзера
    https://djoser.readthedocs.io/en/latest/settings.html#serializers
    """

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
        """
        Узнаем статус подписки
        """

        return SerializerMethods().check_is_subscribed(self.context, obj)


class UserRegSerializer(UserCreateSerializer):
    """
    Cериализатор регистрации
    https://djoser.readthedocs.io/en/latest/settings.html#serializers
    """

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
        )


class CheckSubscribeSerializer(ModelSerializer):
    """
    Просмотр подписок юзера
    """

    recipes = SerializerMethodField()
    is_subscribed = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        ]

    def check_user(self, data):
        user = data['request'].user
        if not user:
            return False
        return user

    def get_is_subscribed(self, obj):
        if user := self.check_user(self.context):
            return bool(obj.user.filter(user=user))
        return False

    def get_recipes(self, obj):
        request = self.context.get('request')
        data = Recipe.objects.filter(author=obj)
        return ShowFavoriteSerializer(
            SerializerMethods().paginator(request, data),
            many=True,
            context=dict(request=request)
        ).data

    def get_recipes_count(self, obj):
        return len(Recipe.objects.filter(author=obj))


class SubscribeSerializer(ModelSerializer):
    """
    Подписки
    """

    class Meta:
        model = Subscription
        fields = ('author', 'user')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('author', 'user'),
            )
        ]

    def validate(self, data):
        if data['user'] != data['author']:
            return data
        raise ValidationError(dict(error='Нельзя подписаться на самого себя'))

    def to_representation(self, data):
        return CheckSubscribeSerializer(
            data.author,
            context=dict(request=self.context.get('request'))
        ).data
