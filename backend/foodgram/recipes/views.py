from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from recipes.filter import FilterIngredient, FilterRecipe
from utils.const import MethodConst
from utils.get_load import dowload_ingredients
from recipes.models import (Favorite, Ingredient, Recipe,
                            ShopCart, Tag)
from recipes.serializer import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientsSerializer, RecipeSerializer,
                          ShopCartSerializer, TagsSerializer)


class TagViewSet(ModelViewSet):
    '''
    Теги
    '''
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    '''
    CRUD рецептов
    '''

    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = FilterRecipe

    def get_serializer_class(self):
        '''
        Выбираем сериализатор в зависимости от типа
        запроса
        '''
        if self.request.method == MethodConst.GET:
            return RecipeSerializer
        return CreateRecipeSerializer


class FavoriteAPIView(APIView):
    '''
    CRUD избранного
    '''

    permission_classes = (IsAuthenticated, )

    def delete(self, request, id):
        try:
            Favorite.objects.filter(user=request.user, recipe_id=id).delete()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, id):
        serializer = FavoriteSerializer(
                data=dict(user=request.user.id, recipe=id),
                context=dict(request=request)
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(dict(errors='Рецепт уже в избранном'), status=status.HTTP_400_BAD_REQUEST)

class IngredientViewSet(ModelViewSet):
    '''
    Ингредиенты
    '''

    pagination_class = None
    serializer_class = IngredientsSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (FilterIngredient, )
    search_fields = ('^name', )


class ShopCartAPIView(APIView):
    '''
    CRUD корзины
    '''

    permission_classes = (IsAuthenticated, )

    def post(self, request, id):
        serializer = ShopCartSerializer(
                data=dict(
                    user=request.user.id,
                    recipe=id
                ),
                context=dict(request=request)
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            ShopCart.objects.filter(user=request.user, recipe_id=id).delete()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadFilesAPIView(APIView):

    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        return HttpResponse(
            '\n'.join(dowload_ingredients(request)),
            'Content-Type: application/pdf'
        )


class MyTest(APIView):
    
    def get(self, *args, **kwargs):
        """from django.contrib.auth import get_user_model
        User = get_user_model()
        DATA_USER = (
            ('usr_test_1', 'usr_test_1', 'usr_test_1', '1@1.ru'),
            ('usr_test_2', 'usr_test_2', 'usr_test_2', '2@2.ru'),
            ('usr_test_3', 'usr_test_3', 'usr_test_3', '3@3.ru'),
            ('usr_test_4', 'usr_test_4', 'usr_test_4', '4@4.ru'),
        )

        for obj in DATA_USER:
            user = User.objects.create_user(
                username=obj[0],
                last_name=obj[1],
                first_name=obj[2],
                email=obj[3],
                password='usr_test_password'
            )
            user.save()
        creacte_admin = User.objects.create_user(
            username='admin',
            last_name='admin',
            first_name='admin',
            email='0@0.ru',
            password='0',
            is_staff = 1,
            is_superuser = 1
        )
        creacte_admin.save()"""
        DATA = (
            ('Рецепт_1', 'Текст рецепта 1', 10),
            ('Рецепт_2', 'Текст рецепта 2', 20),
            ('Рецепт_3', 'Текст рецепта 3', 30),
            ('Рецепт_4', 'Текст рецепта 4', 40),
            ('Рецепт_5', 'Текст рецепта 5', 50),
            ('Рецепт_6', 'Текст рецепта 6', 60),
            ('Рецепт_7', 'Текст рецепта 7', 70),
            ('Рецепт_8', 'Текст рецепта 8', 80),
            ('Рецепт_9', 'Текст рецепта 9', 90),
            ('Рецепт_10', 'Текст рецепта 10', 100),
        )

        from random import randint
        from users.models import User
        from utils.method_serializer import SerializerMethods
        from recipes.models import TagRecipe
        for num in range(1, 100):
            recipe = Recipe.objects.create(
                    author_id = randint(1, 3),
                    name = f'Рецепт {num}',
                    text = f'Текст рецепта {num}',
                    time_cook = randint(1, 150),
                    image=f'recipes/images/data/{randint(1, 11)}.jpg'
                )
            ingredients = (
                dict(
                    id=randint(1, 1000),
                    amount=randint(1, 100)
                    ),
                )
            tags = [id_ for id_ in range(randint(1, 3), 4)]
            SerializerMethods().add_ingredients(ingredients, recipe)
            #SerializerMethods().add_tags(tags, data)
            TagRecipe.objects.bulk_create(
                [
                    TagRecipe(
                        recipe_id=recipe.id,
                        tag_id=tag
                    ) for tag in tags
                ]
            )










