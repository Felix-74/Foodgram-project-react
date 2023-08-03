from django.core.management.base import BaseCommand
from utils.load_ingredient import load_to_db
from utils.create_test_user_and_recipe import CreateTestData

class Command(BaseCommand):

    def handle(self, *args, **options):
        load_to_db()
        test_bool = CreateTestData()()
        self.stdout.write(self.style.SUCCESS(f'Если БД была пуста, данные загружены! {test_bool}'))