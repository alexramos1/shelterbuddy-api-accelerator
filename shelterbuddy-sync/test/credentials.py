from os import getenv
from urllib.parse import quote

shelterbuddyUrl = getenv("SHELTERBUDDY_API_URL")
username = quote(getenv("SHELTERBUDDY_API_USER"))
password = quote(getenv("SHELTERBUDDY_API_PASSWORD"))
