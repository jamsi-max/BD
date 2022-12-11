import asyncpg
import asyncio
from random import sample


def load_common_word() -> list[str]:
    with open('common_words.txt', 'r') as f:
        return f.readlines()


def generate_brand_name(words: list[str]) -> list[tuple[str]]:
    return [(words[index],) for index in sample(range(100), 100)]


async def insert_brands(common_words: list[str], connection: asyncpg.connect) -> int:
    brands: list[tuple[str]] = generate_brand_name(common_words)
    insert_brand: str = "INSERT INTO brand VALUES (DEFAULT, $1)"
    return await connection.executemany(insert_brand, brands)


async def main() -> None:
    common_words = load_common_word()
    conn = await asyncpg.connect(host='127.0.0.1',
                                 port=5432,
                                 user='user',
                                 password='test',
                                 database='products')
    await insert_brands(common_words, conn)

    await conn.close()


if __name__ == '__main__':
    asyncio.run(main())



