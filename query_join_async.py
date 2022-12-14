import asyncpg
import asyncio
from asyncpg import Pool


from tools import async_timed


product_query = \
        """
        SELECT
        p.product_id,
        p.product_name,
        p.brand_id,
        s.sku_id,
        pc.product_color_name,
        ps.product_size_name
        FROM product as p
        JOIN sku as s ON s.product_id = p.product_id
        JOIN product_color as pc ON pc.product_color_id = s.product_color_id
        JOIN product_size as ps ON ps.product_size_id = s.product_size_id
        WHERE p.product_id = 100"""


async def query_product(pool: Pool):
    async with pool.acquire() as conn:
        return await conn.fetchrow(product_query)


@async_timed()
async def query_product_synchronously(pool: Pool, queries: int):
    return [await query_product(pool) for _ in range(queries)]


@async_timed()
async def query_product_async(pool: Pool, queries: int):
    query_list = [query_product(pool) for _ in range(queries)]
    return await asyncio.gather(*query_list)

@async_timed()
async def main():
    async with asyncpg.create_pool(host='127.0.0.1',
                                   port=5432,
                                   user='user',
                                   password='test',
                                   database='products',
                                   min_size=6,
                                   max_size=6) as pool:
        # synvhronous query
        await query_product_synchronously(pool, 10_000)
        # asynchronous query
        await query_product_async(pool, 10_000)


if __name__ == '__main__':
    asyncio.run(main())