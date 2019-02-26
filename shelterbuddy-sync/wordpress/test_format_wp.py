import wp_article_format
import json
from wordpress import create
from os import getenv

endpoint = {
    "url": getenv("WORDPRESS_URL"),
    "username": getenv("WORDPRESS_USER"),
    "password": getenv("WORDPRESS_PASSWORD")
}

f = open("animals.json", "r")

data = json.loads(f.read())

for animal in data[0:9]:

    article = wp_article_format.animal(animal, lambda x: "")

    title = animal['Name']
    title += " - " + animal['Sex']['Name']
    title += " " + animal['Breed']['Primary']['Name']
    title += " - " + animal['ContactLocation']['Name']

    params = {
        'title': title + " #" + str(animal['Id']),
        'content': article,
        'exerpt': title,
        'status': 'publish'
    }

    rs = create(endpoint, params)
