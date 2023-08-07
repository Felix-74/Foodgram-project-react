from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from recipes.filter import FilterIngredient, FilterRecipe
from utils.const import MethodConst
from utils.get_load import dowload_ingredients
from recipes.models import Ingredient, Recipe, Tag
from recipes.serializer import (CreateRecipeSerializer, FavoriteSerializer,
                                IngredientsSerializer, RecipeSerializer,
                                ShopCartSerializer, TagsSerializer)


class TagViewSet(ModelViewSet):
    """
    Теги
    """
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """
    CRUD рецептов
    """

    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = FilterRecipe

    def get_serializer_class(self):
        """
        Выбираем сериализатор в зависимости от типа
        запроса
        """
        if self.request.method == MethodConst.GET:
            return RecipeSerializer
        return CreateRecipeSerializer


class FavoriteAPIView(APIView):
    """
    CRUD избранного
    """

    permission_classes = (IsAuthenticated, )

    def delete(self, request, id):
        self.request.user.favorite.filter(recipe_id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, id):
        serializer = FavoriteSerializer(
                data=dict(user=request.user.id, recipe=id),
                context=dict(request=request)
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)


class IngredientViewSet(ModelViewSet):
    """
    Ингредиенты
    """

    pagination_class = None
    serializer_class = IngredientsSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (FilterIngredient, )
    search_fields = ('^name', )


class ShopCartAPIView(APIView):
    """
    CRUD корзины
    """

    permission_classes = (IsAuthenticated, )

    def post(self, request, id):
        serializer = ShopCartSerializer(
                data=dict(
                    user=request.user.id,
                    recipe=id
                ),
                context=dict(request=request)
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        self.request.user.shop_cart.filter(recipe_id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadFilesAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return HttpResponse(
            '\n'.join(dowload_ingredients(request)),
            'Content-Type: application/pdf'
        )
