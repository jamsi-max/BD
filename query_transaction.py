import asyncio
import asyncpg
import logging

from asyncpg.transaction import Transaction

async def main():
    conn = await asyncpg.connect(host='127.0.0.1',
                                 port=5432,
                                 user='user',
                                 password='test',
                                 database='products')
    # EXAMPLE # 1
    # try:
    #     async with conn.transaction():
    #         insert_brand = "INSERT INTO brand VALUES(1000, 'small_brand')"
    #         await conn.execute(insert_brand)
    #         await conn.execute(insert_brand)
    # except Exception as e:
    #     logging.exception('Exception transaction run')
    # finally:
    #     query = """SELECT brand_name FROM brand
    #                WHERE brand_name LIKE 'small%'"""
    #     brands = await conn.fetch(query)
    #     print(f'Result: {brands}')
    #     await conn.close()

    # EXAMPLE #2
    # async with conn.transaction():
    #     await conn.execute("INSERT INTO brand VALUES(DEFAULT, 'my_new_brand')")
    #
    #     try:
    #         async with conn.transaction():
    #             await conn.execute("INSERT INTO product_color VALUES(1, 'black')")
    #     except Exception as e:
    #         logging.exception('Exception insert to table "product_color"', exc_info=e)
    # await conn.close()

    # EXAMPLE #3

    transaction: Transaction = conn.transaction()
    await transaction.start()
    try:
        await conn.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_3')")
        await conn.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_4')")
    except asyncpg.PostgresError as e:
        logging.exception('Exception transaction')
        await transaction.rollback()
    else:
        print('Transaction is done')
        await transaction.commit()

    query = """SELECT brand_name FROM brand
               WHERE brand_name LIKE 'brand%'"""
    brands = await conn.fetch(query)
    print(f'Result: {brands}')
    await conn.close()


if __name__ == '__main__':
    asyncio.run(main())
