import httpx
import asyncio
from datetime import datetime
from sqlalchemy import insert
from db.models import Language, RawPost
from db.database import AsyncSessionLocal

SITE_URL = "https://mastodon.social/api/v1/timelines/tag/"
SEARCH_QUERY = "infantino"
url = f"{SITE_URL}/{SEARCH_QUERY}"
pages = 20

queue = asyncio.Queue(maxsize=100)

async def scrape():
    max_id = None

    async with httpx.AsyncClient() as client:
        for _ in range(pages):

            params = {"limit": 40}
            if max_id:
                params["max_id"] = max_id

            batch = []

            try:
                response = await client.get(
                    url=url,
                    params=params
                )

            except not response.json():    
                print("No posts found")
                return None
            
            except response.status_code == 429:
                await asyncio.sleep(60)

                        
            posts = response.json()
            
            for post in posts:
                if post['language'] == Language.ENGLISH.value and len(post['content']) > 30:

                    batch.append({
                        "timestamp": datetime.strptime(post['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                        "content": post['content']
                    })

            await queue.put(batch)
            max_id = posts[-1]["id"]

        await queue.put(None)

async def db_insert(batch):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(
                insert(RawPost),
                batch
            )

async def db_ingest():
    while True:
        batch = await queue.get()

        if not batch:
            queue.task_done()
            break
        try:
            await db_insert(batch)
        except Exception as e:
            print("Error: " + e)
        finally:
            queue.task_done()

async def main():
    await asyncio.gather(scrape(), db_ingest())

if __name__ == "__main__":
    asyncio.run(main())