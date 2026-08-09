import asyncio
from db.database import init_db, AsyncSessionLocal
from db.models import RawPost
from sqlalchemy import select
# Step 1
# Fetch new row added to the database not processed yet
async def fetch():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            data = await session.execute(select(RawPost))
        return data.scalars().all() 

async def main():
    await init_db()
    data = await fetch()
    print(data)

if __name__ == "__main__":
    asyncio.run(main())
# posts =  await fetch()
# print(fetch())
# Step 2
# Process the new data 

# step 3
# Ingest the newly-processed data into the database