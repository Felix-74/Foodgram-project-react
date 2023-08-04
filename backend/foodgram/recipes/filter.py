from rest_framework.filters import SearchFilter
from django_filters.rest_framework import (BooleanFilter,
                                           ModelMultipleChoiceFilter,
                                           CharFilter, FilterSet)

from recipes.models import Recipe, Tag


class FilterRecipe(FilterSet):
    '''
    Фильтра рецептов
    https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html
    '''

    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='filter_shopping_cart')
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    author = CharFilter()

    class Meta:
        model = Recipe
        fields = ("shopping_cart", "favorite", "tags", "author")

    def filter_is_favorited(self, queryset, _, value):
        '''
        Фильтрация queryset'a избранного
        '''
        if not value:
            return queryset
        return queryset.filter(favorite__user=self.request.user)

    def filter_shopping_cart(self, queryset, _, value):
        '''
        Фильтрация корзины
        '''
        if not value:
            return queryset
        return queryset.filter(shopping_cart__user=self.request.user)


class FilterIngredient(SearchFilter):
    '''
    Фильтр ингредиентов по имени
    '''
    search_param = 'name'
