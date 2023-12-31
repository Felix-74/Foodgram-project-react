import json
from recipes.models import Ingredient, Tag


TAG_DATA = (
    ('Завтрак', '#CD5C5C', 'breakfast'),
    ('Обед', '#ADFF2F', 'lunch'),
    ('Ужин', '#FFFF00', 'dinner')
)


def load_to_db():
    """
    Загрузка данных в БД если она пуста
    """
    resp_ = {}
    if len(Tag.objects.all()) == 0:
        Tag.objects.bulk_create([
            Tag(
                name=tag_[0],
                color=tag_[1],
                slug=tag_[2]
            ) for tag_ in TAG_DATA
        ])
        resp_.update(dict(tag_load='Теги загружены!'))
    else:
        resp_.update(dict(tag_load='Теги не загружены!'))
    if len(Ingredient.objects.all()) == 0:
        with open('utils/data/ingredients.json', 'r') as f:
            Ingredient.objects.bulk_create([
                Ingredient(
                    measurement_unit=obj['measurement_unit'],
                    name=obj['name']
                ) for obj in json.load(f)
            ])
        resp_.update(dict(ingredient_load='Ингредиенты загружены!'))
    else:
        resp_.update(dict(ingredient_load='Ингредиенты не загружены!'))
