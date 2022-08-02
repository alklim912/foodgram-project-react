import json

from django.core.management.base import BaseCommand
from psycopg2 import connect

from foodgram.settings import DATABASES


def get_cursor(db_string, values):
    DATABASE = DATABASES['default']
    connection = connect(
        dbname=DATABASE.get('NAME'),
        user=DATABASE.get('USER'),
        password=DATABASE.get('PASSWORD'),
        host=DATABASE.get('HOST'),
        port=DATABASE.get('PORT')
    )
    cursor = connection.cursor()
    cursor.execute(db_string, values)
    connection.commit()
    connection.close()


class Command(BaseCommand):
    help = 'Load Tags and Ingredient'

    def handle(self, *args, **options):
        if options['tags']:
            traffic = json.load(open('data/tags.json', encoding='utf-8'))
            id = 0
            for row in traffic:
                id += 1
                name = row['name']
                color = row['color']
                slug = row['slug']
                get_cursor(
                    'INSERT INTO app_tag (id, name, color, slug)'
                    'VALUES (%s, %s, %s, %s)',
                    (id, name, color, slug)
                )
        if options['ingredients']:
            traffic = json.load(open(
                'data/ingredients.json', encoding='utf-8'))
            id = 0
            for row in traffic:
                id += 1
                name = row['name']
                measurement_unit = row['measurement_unit']
                get_cursor(
                    'INSERT INTO app_ingredient (id, name, measurement_unit)'
                    'VALUES (%s, %s, %s)',
                    (id, name, measurement_unit)
                )

    def add_arguments(self, parser):
        parser.add_argument(
            '--tags',
            action='store_true',
            help='Загрузка тегов'
        )
        parser.add_argument(
            '--ingredients',
            action='store_true',
            help='Загрузка ингредиентов'
        )
