import json

from psycopg2 import connect

from foodgram.settings import DATABASES

DATABASE = DATABASES['default']

connection = connect(
    dbname=DATABASE.get('NAME'),
    user=DATABASE.get('USER'),
    password=DATABASE.get('PASSWORD'),
    host=DATABASE.get('HOST'),
    port=DATABASE.get('PORT')
)
cursor = connection.cursor()

traffic = json.load(open('data/ingredients.json', encoding='utf-8'))
columns = ['name', 'measurement_unit']
id = 0
for row in traffic:
    id += 1
    name = row['name']
    measurement_unit = row['measurement_unit']
    cursor.execute(
        'INSERT INTO app_ingredient (id, name, measurement_unit)'
        'VALUES (%s, %s, %s)',
        (id, name, measurement_unit)
    )


traffic = json.load(open('data/tags.json', encoding='utf-8'))
columns = ['name', 'color', 'slug']
id = 0
for row in traffic:
    id += 1
    name = row['name']
    color = row['color']
    slug = row['slug']
    cursor.execute(
        'INSERT INTO app_tag (id, name, color, slug) VALUES (%s, %s, %s, %s)',
        (id, name, color, slug)
    )

connection.commit()
connection.close()
