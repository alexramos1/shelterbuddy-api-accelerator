from wordpress import create
from os import getenv

endpoint = {
    "url": getenv("WORDPRESS_URL"),
    "username": getenv("WORDPRESS_USER"),
    "password": getenv("WORDPRESS_PASSWORD")
}

rs = create(endpoint, "test")

print(rs)
