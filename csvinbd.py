import json
import sqlite3

connection = sqlite3.connect('backend/foodgram/db.sqlite3')
cursor = connection.cursor()

traffic = json.load(open('data/ingredients.json', encoding='utf-8'))
columns = ['name', 'measurement_unit']
id = 0
for row in traffic:
    id += 1
    name = row['name']
    measurement_unit = row['measurement_unit']
    cursor.execute(
        'insert into app_ingredient values(?,?,?)',
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
        'insert into app_tag values(?,?,?,?)',
        (id, name, color, slug)
    )

connection.commit()
connection.close()
