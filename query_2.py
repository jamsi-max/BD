import asyncpg
import asyncio
from asyncpg import Record
from typing import List


async def main():
    conn = await asyncpg.connect(host='127.0.0.1',
                                 port=5432,
                                 user='user',
                                 password='test',
                                 database='products')


    # query = 'SELECT COUNT(*) FROM sku'
    query = \
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
    # query = \
    #     """
    #     SELECT
    #     product_name
    #     FROM product
    #     WHERE product_id = 100"""
    results: List[Record] = await conn.fetch(query)
    # print(results)
    for r in results:
        print(f'id: {r["product_id"]},'
              f'name: {r["product_name"].strip()},'
              f'brand_id: {r["brand_id"]},'
              f'sku_id: {r["sku_id"]},'
              f'product_color_name: {r["product_color_name"]},'
              f'product_size_name: {r["product_size_name"]}')
    await conn.close()


if __name__ == '__main__':
    asyncio.run(main())
