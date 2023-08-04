from recipes.models import Favorite, ShopCart
from users.models import Subscription
from recipes.models import (Ingredient, IngredientRecipe,
                            TagRecipe)


class SerializerMethods:

    '''
    Будет использоваться в нескольких сериализаторах,
    что бы не нарушать DRY, вынес в utils
    '''

    def paginator(self, request, recipes):
        limit = request.query_params.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        return recipes

    def check_is_user(self, context):
        request = context.get('request', None)
        if request and request.user.is_anonymous:
            return False
        return True

    def check_request_context(self, context):
        if context.get('request', False):
            return False
        return True

    def check_is_favorited(self, context, obj):
        if self.check_is_user(context):
            return Favorite.objects.filter(
                user=context['request'].user, recipe_id=obj.id
            ).exists()
        return False

    def check_is_subscribed(self, context, obj):
        if self.check_is_user(context):
            return Subscription.objects.filter(
                user_id=context['request'].user.id, author_id=obj.id
            ).exists()
        return False

    def check_in_shopping_cart(self, context, obj):
        if self.check_is_user(context):
            return ShopCart.objects.filter(
                user=context['request'].user, recipe_id=obj.id
            ).exists()
        return False

    def add_ingredients(self, data_ingredient, recipe):
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    ingredient=Ingredient.objects.get(
                        id=obj_ingredient.get('id')
                    ),
                    recipe=recipe,
                    amount=obj_ingredient.get('amount')
                ) for obj_ingredient in data_ingredient
            ]
        )

    def add_tags(self, tags, recipe):
        TagRecipe.objects.bulk_create(
            [
                TagRecipe(
                    recipe=recipe,
                    tag=tag
                ) for tag in tags
            ]
        )
