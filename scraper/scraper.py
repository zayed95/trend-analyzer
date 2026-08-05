import json
import re
import asyncio
import requests
from datetime import datetime
from sqlalchemy.ext.asyncio.session import AsyncSession
from db.models import Language, RawPost
from db.database import get_session, init_db

SITE_URL = "https://mastodon.social/api/v1/timelines/tag/"
SEARCH_QUERY = "infantino"
url = f"{SITE_URL}/{SEARCH_QUERY}"
max_id = 0

def scrape(limit: int = 20):

    scraped_posts = []

    while len(scraped_posts) < limit:

        response = requests.get(url=url)
        if response.status_code == 200:
            posts = response.json()
            if not posts:
                return None

            for post in posts:
                if post['language'] == Language.ENGLISH.value and len(post['content']) > 30:
                    
                    scraped_posts.append({
                        "timestamp": post['content'],
                        "content": datetime.fromisoformat(post['created_at'].replace("Z", "+00:00"))
                    })

                    max_id = post['id']

            return scraped_posts
        print("Error")
        return None


async def ingest(posts: list):

    if not posts or len(posts) == 0:
        print("Error: no posts found!")
        return None

    await init_db()
    session =  get_session()

    for post in posts:
        raw_post = RawPost(**post)
        session.add(raw_post)
        await session.commit()
        await session.refresh(raw_post)

    print("All done!")

posts = scrape()
asyncio.run(ingest(posts)) 