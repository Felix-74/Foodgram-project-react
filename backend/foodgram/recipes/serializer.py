import datetime

from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        ReadOnlyField,
                                        IntegerField,
                                        PrimaryKeyRelatedField)
from recipes.models import (Tag, Ingredient, Recipe,
                            IngredientRecipe, TagRecipe,
                            Favorite, ShopCart)
from utils.method_serializer import SerializerMethods
from users.models import User


from drf_extra_fields.fields import Base64ImageField
from rest_framework.validators import ValidationError

class IngredientRecipeSerializer(ModelSerializer):
    '''
    Связывающий сериализатор ингредиентов и рецепта
    '''

    name = ReadOnlyField(source='ingredient.name')
    id = ReadOnlyField(source='ingredient.id')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount', 'measurement_unit', 'name')

class TagsSerializer(ModelSerializer):
    '''
    Сериализатор тегов
    '''

    class Meta:
        model = Tag
        fields = ('id', 'color', 'slug', 'name')


class IngredientsSerializer(ModelSerializer):
    '''
    (GET) Сериализатор ингредиентов
    '''

    class Meta:
        model = Ingredient
        fields = ('id', 'measurement_unit', 'name')

class AuthorSerializer(DjoserUserSerializer):
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
        return SerializerMethods().check_is_subscribed(self.context, obj)

class RecipeSerializer(ModelSerializer):
    '''
    Сериализатор рецепта
    '''


    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    tags = TagsSerializer(many=True)
    author = AuthorSerializer()
    cooking_time = IntegerField(source='time_cook')

    class Meta:
        model = Recipe
        fields = '__all__'
        #exclude = ('time_cook',)
        read_only_fields = ('author',)


    def get_ingredients(self, obj):
        return IngredientRecipeSerializer(
            IngredientRecipe.objects.filter(recipe=obj),
            many=True
        ).data


    def get_is_in_shopping_cart(self, obj):
        return SerializerMethods().check_in_shopping_cart(self.context, obj)


    def get_is_favorited(self, obj):
        return SerializerMethods().check_is_favorited(self.context, obj)


class CreateIngredientRecipe(ModelSerializer):
    '''
    Добавление ингредиента в рецепт
    '''
    
    id = IntegerField()
    amount = IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class CreateRecipeSerializer(ModelSerializer):
    '''
    Создать/обновить рецепт
    '''

    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()
    author = DjoserUserSerializer(read_only=True) #UserSerializer(read_only=True)
    ingredients = CreateIngredientRecipe(many=True)
    cooking_time = IntegerField(source='time_cook')


    class Meta:
        model = Recipe
        fields = ('name',
                  'cooking_time',
                  #'time_cook',
                  'text',
                  'tags',
                  'author',
                  'ingredients',
                  'image',
                  'date_add')

    def add_tag_and_ingredient(self, tags, ingredients, data):
        SerializerMethods().add_ingredients(ingredients, data)
        SerializerMethods().add_tags(tags, data)

    def create(self, validated_data):
        '''
        Добавить рецепт
        '''

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            **validated_data
        )
        self.add_tag_and_ingredient(tags, ingredients, recipe)
        return recipe

    def update(self, data, validated_data):
        '''
        Изменение рецепта
        '''

        IngredientRecipe.objects.filter(recipe=data).delete()
        TagRecipe.objects.filter(recipe=data).delete()

        ingredients = validated_data.get('ingredients', False)
        tags = validated_data.get('tags', False)
        self.add_tag_and_ingredient(tags, ingredients, data)
        data.text = validated_data.get('text', False)
        data.image = validated_data.get('image', False)
        data.time_cook = validated_data.get('time_cook', False)
        data.name = validated_data.get('name', False)
        data.date_add = datetime.datetime.utcnow()
        data.save()
        return data

    def to_representation(self, data):
        return RecipeSerializer(
            data,
            context=dict(request=self.context.get('request'))
        ).data
        

class ShowFavoriteSerializer(ModelSerializer):
    '''
    Показать избранное
    '''

    cooking_time = IntegerField(source='time_cook')

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')
        
        
class FavoriteSerializer(ModelSerializer):
    '''
    Избранное
    '''

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        if Favorite.objects.filter(user_id=data['user'], recipe__id=data['recipe'].id).exists():
            raise ValidationError("Уже есть такая подписка!")
        return data


    def to_representation(self, data):
        return ShowFavoriteSerializer(
            data.recipe,
            context=dict(request=self.context.get('request'))
        ).data


class ShopCartSerializer(ModelSerializer):
    '''
    Сериализатор корзины
    '''

    class Meta:
        model = ShopCart
        fields = ('user', 'recipe')

    def validate(self, data):
        if ShopCart.objects.filter(user_id=data['user'], recipe_id=data['recipe'].id).exists():
            raise ValidationError("Предмет уже добавлен!!")
        return data

    def to_representation(self, data):
        
        return ShowFavoriteSerializer(
            data.recipe,
            context=dict(request=self.context.get('request'))
        ).data

class RecipesSubsSerializer(RecipeSerializer):
    
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')