from cloudflare_worker import MY_KV


async def kv_get(key: str):
    return await MY_KV.get(key)


async def kv_put(key: str, value: str):
    await MY_KV.put(key, value)
    return {"status": "put"}


async def kv_patch(key: str, value: str):
    await MY_KV.put(key, value)
    return {"status": "patched"}


async def kv_delete(key: str):
    await MY_KV.delete(key)
    return {"status": "deleted"}
