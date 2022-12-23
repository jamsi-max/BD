import asyncio
import asyncpg

from tools import async_timed


# example offset 500 records and get 100 records with 501 to 600
@async_timed()
async def main():
    conn = await asyncpg.connect(host='127.0.0.1',
                                 port=5432,
                                 user='user',
                                 password='test',
                                 database='products')

    query = "SELECT product_id, product_name FROM product"
    async with conn.transaction():
        # prefetch set max load data in database
        async for item in conn.cursor(query, prefetch=10):
            print(item)

    await conn.close()


@async_timed()
async def main():
    conn = await asyncpg.connect(host='127.0.0.1',
                                 port=5432,
                                 user='user',
                                 password='test',
                                 database='products')

    async with conn.transaction():
        query = "SELECT product_id, product_name FROM product"
        cursor = await conn.cursor(query)
        await cursor.forward(500)
        products = await cursor.fetch(100)

        for item in products:
            print(item)

    await conn.close()

if __name__ == '__main__':
    asyncio.run(main())
