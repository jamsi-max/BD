import asyncpg
import asyncio
from random import randint, sample
from query_insert_brand import load_common_word


def gen_products(common_word: list[str],
                 brand_id_start: int,
                 brand_id_end: int,
                 products_to_create: int) -> list[tuple[str, int]]:
    products: list = []
    for _ in range(products_to_create):
        description:  list = [common_word[index] for index in sample(range(1000), 10)]
        brand_id: int = randint(brand_id_start, brand_id_end)
        products.append((" ".join(description), brand_id))
    return products


def gen_sku(product_id_start: int,
            product_id_end: int,
            skus_to_create: int) -> list[tuple[int, int, int]]:
    skus: list = []
    for _ in range(skus_to_create):
        product_id: int = randint(product_id_start, product_id_end)
        size_id: int = randint(1,3)
        color_id: int = randint(1,2)
        skus.append((product_id, size_id, color_id))
    return skus


async def main() -> None:
    common_words = load_common_word()
    conn = await asyncpg.connect(host='127.0.0.1',
                                 port=5432,
                                 user='user',
                                 password='test',
                                 database='products')

    product_tuples: list[tuple[str, int]] = gen_products(common_words,
                                                         brand_id_start=7,
                                                         brand_id_end=106,
                                                         products_to_create=1000)
    await conn.executemany('INSERT INTO product VALUES (DEFAULT, $1, $2)', product_tuples)

    sku_tuples: list[tuple[int, int, int]] = gen_sku(product_id_start=56,
                                                     product_id_end=1_155,
                                                     skus_to_create=100_000)
    await conn.executemany('INSERT INTO sku VALUES (DEFAULT, $1, $2, $3)', sku_tuples)

    await conn.close()


if __name__ == '__main__':
    asyncio.run(main())