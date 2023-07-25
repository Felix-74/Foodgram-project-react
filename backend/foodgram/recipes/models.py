from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

User = get_user_model()


class Recipe(models.Model):
    '''
    Рецепт
    '''

    name = models.CharField('Рецепт', max_length=140)
    text = models.TextField(
        'Описание рецепта',
        help_text='Заполните описание рецепта'
    )
    tags = models.ManyToManyField(
        'Tag',
        through='TagRecipe',
        related_name='tags'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientRecipe',
        verbose_name='Ингредиенты'
    )
    time_cook = models.PositiveIntegerField(
        verbose_name='Время готовки',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/'
    )
    date_add = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )


class Ingredient(models.Model):
    '''
    Ингредиент
    '''

    measurement_unit = models.CharField('Тип измерения', max_length=140)
    name = models.CharField(
        'Ингредиент',
        max_length=140,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        constraints = [
            UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_constraint_ingredient_name_unit'
            )
        ]


class Tag(models.Model):
    '''
    Тег
    '''

    slug = models.SlugField('Слаг', unique=True, max_length=140)
    name = models.CharField('Название тега', unique=True, max_length=140)
    color = models.CharField('HEX', unique=True, max_length=7)

    class Meta:

        verbose_name = 'Тег'


class Favorite(models.Model):
    '''
    Избранное
    '''

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Юзер',
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_constraint_user_favorite'
            )
        ]


class IngredientRecipe(models.Model):
    '''
    Промежуточная модель таблицы ингредиента и рецепта
    '''

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField('Количество')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_constraint_recipe_ingredient'
            )
        ]


class TagRecipe(models.Model):
    '''
    Промежуточная модель таблицы тега и рецепта
    '''

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('recipe', 'tag'),
                name='unique_constraint_recipe_tag'
            )
        ]


class ShopCart(models.Model):
    '''
    Корзина покупок
    '''

    user = models.ForeignKey(
        User,
        verbose_name='Юзер',
        related_name='shop_cart',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='shopping_cart',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_constraint_shop_cart'
            )
        ]
