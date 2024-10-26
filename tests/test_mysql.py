import asyncio

import asyncmy

from conftest import client

index = client.index("mysql")


async def test_sync():
    conn = await asyncmy.connect(
        host="localhost",
        user="root",
        password="123456",
        port=3306,
        database="test",
    )
    async with conn.cursor() as cur:
        await cur.execute("DROP TABLE IF EXISTS test")
        await cur.execute(
            "CREATE TABLE IF NOT EXISTS test (id INT PRIMARY KEY, age INT, time timestamp NOT NULL)"
        )
        await cur.execute(
            "INSERT INTO test (id, age, time) VALUES (%s, %s, %s)",
            (1, 46, "1977-01-27 22:00:53"),
        )
        await conn.commit()
    await asyncio.sleep(2)
    ret = await index.get_documents()
    assert ret.results == [{"id": 1, "age": 46, "time": 223250453}]
