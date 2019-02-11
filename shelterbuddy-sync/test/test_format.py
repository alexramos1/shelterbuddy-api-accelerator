import article_format
import json

f = open("animals.json", "r")

data = json.loads(f.read())

print(article_format.animal(data[0], lambda x: "resolve(" + x + ")"))