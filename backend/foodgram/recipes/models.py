from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError
from utils.validators import min_max_small_int

User = get_user_model()


class Recipe(models.Model):
    """
    Рецепт
    """

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
    time_cook = models.PositiveSmallIntegerField(
        verbose_name='Время готовки'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/'
    )
    date_add = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-date_add',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        """
        Для правильного отображения в админке
        """
        return self.name

    def clean(self):
        if min_max_small_int(self.time_cook):
            raise ValidationError("Не верное значение времени готовки")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Ingredient(models.Model):
    """
    Ингредиент
    """

    measurement_unit = models.CharField('Тип измерения', max_length=140)
    name = models.CharField(
        'Ингредиент',
        max_length=140,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        """
        Для правильного отображения в админке
        """
        return self.name


class Tag(models.Model):
    """
    Тег
    """

    slug = models.SlugField('Слаг', unique=True, max_length=140)
    name = models.CharField('Название тега', unique=True, max_length=140)
    color = models.CharField('HEX', unique=True, max_length=7)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        """
        Для правильного отображения в админке
        """
        return self.name


class Favorite(models.Model):
    """
    Избранное
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Юзер',
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
    """
    Промежуточная модель таблицы ингредиента и рецепта
    """

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
    amount = models.PositiveSmallIntegerField('Количество')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_constraint_recipe_ingredient'
            )
        ]

    def clean(self):
        if min_max_small_int(self.amount):
            raise ValidationError("Не верное значение кол-ва ингредиента")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class TagRecipe(models.Model):
    """
    Промежуточная модель таблицы тега и рецепта
    """

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
    """
    Корзина покупок
    """

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
