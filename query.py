import asyncpg
import asyncio
from asyncpg import Record
from typing import List


async def main():
    conn = await asyncpg.connect(host='127.0.0.1',
                                 port=5432,
                                 user='user',
                                 password='test',
                                 database='products'
                                 )
    await conn.execute("INSERT INTO brand VALUES(DEFAULT, 'Levis')")
    await conn.execute("INSERT INTO brand VALUES(DEFAULT, 'Seven')")

    brand_query = 'SELECT brand_id, brand_name FROM brand'
    results: List[Record] = await conn.fetch(brand_query)
    for brand in results:
        print(type(brand))
        print(f'id: {brand["brand_id"]}, name: {brand["brand_name"]}')
    await conn.close()



if __name__ == '__main__':
    asyncio.run(main())