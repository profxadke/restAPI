from cloudflare_worker import MY_D1


async def get_d1_data(query: str):
    result = await MY_D1.query(query)
    return result


async def insert_d1_data(query: str):
    await MY_D1.execute(query)


async def update_d1_data(query: str):
    await MY_D1.execute(query)


async def delete_d1_data(query: str):
    await MY_D1.execute(query)
