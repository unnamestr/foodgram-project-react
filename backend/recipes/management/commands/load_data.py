from django.core.management import BaseCommand
import json

from recipes.models import Ingredient

TABLES = {
    Ingredient: 'ingredients.json',
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, csv_f in TABLES.items():
            with open(f'../data/{csv_f}', 'r', encoding='utf-8') as file:
                reader = json.loads(file.read())
                model.objects.bulk_create((model(**data) for data in reader), ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
