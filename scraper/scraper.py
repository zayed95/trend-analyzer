import json
from turtle import pos
from urllib import response
import requests
from bs4 import BeautifulSoup
#from mastodon import Mastodon

SITE_URL = "https://mastodon.social/api/v1/timelines/tag/"
SEARCH_QUERY = "infantino"
url = f"{SITE_URL}/{SEARCH_QUERY}"
max_results = 5

def scrape():
    response = requests.get(url=url)
    if response.status_code == 200:
        posts = response.json()
        for post in posts:
            print("content: " + post['content'])
            print("\ntimestamp: " + post['created_at'])
            #print("\nlanguage: " + post['language'])

data = scrape()
print(data)