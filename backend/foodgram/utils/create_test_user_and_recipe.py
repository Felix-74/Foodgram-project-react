from random import randint
from django.contrib.auth import get_user_model

from users.models import User
from utils.method_serializer import SerializerMethods
from recipes.models import TagRecipe, Recipe


DATA_USER = (
    ('usr_test_1', 'usr_test_1', 'usr_test_1', '1@1.ru'),
    ('usr_test_2', 'usr_test_2', 'usr_test_2', '2@2.ru'),
    ('usr_test_3', 'usr_test_3', 'usr_test_3', '3@3.ru'),
    ('usr_test_4', 'usr_test_4', 'usr_test_4', '4@4.ru'),
)


class CreateTestData:

    def __init__(self) -> None:
        self.user_model = get_user_model()

    def __call__(self, *args, **kwds):
        """
        Возможность вызывать класс как функцию
        """
        if check := self.check_db():
            self.create_test_user()
            self.create_admin()
            self.create_test_recipes()
        return check

    def check_db(self):
        """
        Проверка на наличие записей в бд
        """
        usr = len(User.objects.all())
        rec = len(Recipe.objects.all())
        if usr == 0 and rec == 0:
            return True
        return False

    def create_admin(self):
        """
        Создание администратора
        """
        creacte_admin = self.user_model.objects.create_user(
            username='admin',
            last_name='admin',
            first_name='admin',
            email='0@0.ru',
            password='0',
            is_staff=1,
            is_superuser=1
        )
        creacte_admin.save()

    def create_test_user(self):
        """
        Создание обычных пользователей
        """
        for obj in DATA_USER:
            user = self.user_model.objects.create_user(
                username=obj[0],
                last_name=obj[1],
                first_name=obj[2],
                email=obj[3],
                password='usr_test_password'
            )
            user.save()

    def create_test_recipes(self):
        """
        Создание рандомных тестовых рецептов
        """
        for num in range(1, 60):
            recipe = Recipe.objects.create(
                author_id=randint(1, 3),
                name=f'Рецепт {num}',
                text=f'Текст рецепта {num}',
                time_cook=randint(1, 150),
                image=f'recipes/images/data/{randint(1, 11)}.jpg'
            )
            ingredients = (
                dict(id=randint(1, 1000),
                     amount=randint(1, 100)), )
            tags = [id_ for id_ in range(randint(1, 3), 4)]
            SerializerMethods().add_ingredients(ingredients, recipe)
            TagRecipe.objects.bulk_create(
                [
                    TagRecipe(
                        recipe_id=recipe.id,
                        tag_id=tag
                    ) for tag in tags
                ]
            )
            recipe.save()
