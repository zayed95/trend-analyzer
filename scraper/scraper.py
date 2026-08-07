import httpx
import asyncio
from datetime import datetime
from sqlalchemy import insert
from db.models import Language, RawPost, Base
from db.database import AsyncSessionLocal, init_db

SITE_URL = "https://mastodon.social/api/v1/timelines/tag/"

queue = asyncio.Queue(maxsize=100)

async def scrape(query: str, pages: int = 10):
    max_id = None
    url = f"{SITE_URL}/{query}"
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

                posts = response.json()  
                
            
                if response.status_code == 429:
                    await asyncio.sleep(60)
                    continue

            except Exception as e:
                print(f"request error: {e}")         

            if not posts:
                print(f"No posts in that hashtag: {query}")
                break

            for post in posts:
                if post['language'] == Language.ENGLISH.value and len(post['content']) > 30:

                    batch.append({
                        "timestamp": datetime.strptime(post['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                        "content": post['content'],
                        "keyword": query
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
            await session.commit()

async def db_ingest():
    while True:
        batch = await queue.get()

        if batch is None:
            queue.task_done()
            break
        try:
            await db_insert(batch)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            queue.task_done()

async def main():
    await init_db()
    await asyncio.gather(scrape("trump", 1), db_ingest())

if __name__ == "__main__":
    asyncio.run(main())