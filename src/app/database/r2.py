from cloudflare_worker import MY_R2


async def upload_to_r2(file_data: bytes, file_name: str):
    await MY_R2.put(file_name, file_data)
    return {"status": "uploaded"}


async def get_from_r2(file_name: str):
    return await MY_R2.get(file_name)


async def delete_from_r2(file_name: str):
    await MY_R2.delete(file_name)
    return {"status": "deleted"}
