from recipes.models import IngredientRecipe

def dowload_ingredients(request):
    '''
    Собираем ингредиенты из покупок
    '''
    ingredients = IngredientRecipe.objects.filter(
        recipe__shopping_cart__user=request.user
    ).values(
        'amount', 'ingredient__name', 'ingredient__measurement_unit'
    )
    data = {}
    for obj in ingredients:
        name = obj['ingredient__name']
        amount = obj['amount']
        unit = obj['ingredient__measurement_unit']
        if name not in data:
            data[name] = {'name': name, 'amount': amount, 'unit': unit}
        else:
            data[name]['amount'] += amount
    data_list = []
    for obj in data.items():
        objs = f'{obj[1]["name"]} - {obj[1]["amount"]} - {obj[1]["unit"]}'
        data_list.append(objs)
    return data_list