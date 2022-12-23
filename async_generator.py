import asyncio
import asyncpg

from tools import async_timed


async def take(generator, to_take: int):
    item_count = 0
    async for i in generator:
        if item_count > to_take - 1:
            return
        item_count += 1
        yield i


@async_timed()
async def main():
    conn = await asyncpg.connect(host='127.0.0.1',
                                 port=5432,
                                 user='user',
                                 password='test',
                                 database='products')

    async with conn.transaction():
        query = "SELECT product_id, product_name FROM product"
        product_generator = conn.cursor(query)

        async for item in take(product_generator, 5):
            print(item)

    await conn.close()

#  read library import aiostream -> www.aiostream.readthedocs.io
if __name__ == '__main__':
    asyncio.run(main())