import asyncio
import emoji
import re
from db.database import AsyncSessionLocal, engine, Base
from db.models import RawPost, CleanPost
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

# Step 1
# Fetch new row added to the database not processed yet
async def extract(keyword: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            data = await session.execute(select(RawPost).where(RawPost.keyword == keyword))
            return data.scalars().all()

# Step 2
# Process the new data 
def clean(text: str) -> str:
    text = text.lower().strip()
    text = re.sub('<.*?>', '', text)
    text = emoji.demojize(text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'#\w+', '', text)
    return text

def transform(posts: list) -> list:

    clean_posts = []
    for post in posts:

        clean_posts.append({
            "raw_id": post.id,
            "content": clean(post.content),
            "timestamp": post.timestamp,
            "keyword": post.keyword
        })

    return clean_posts

# step 3
# Ingest the newly-processed data into the database 
async def db_insert(batch: list):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            try:
                await session.execute(
                    insert(CleanPost),
                    batch
                )
            except IntegrityError:
                await session.rollback()
        await session.commit()

async def main():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        posts = await extract("trump")
        if posts:
            clean_posts = transform(posts)
            await db_insert(clean_posts)
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main(), debug=True)
