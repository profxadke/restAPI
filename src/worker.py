import asyncio
from fastapi import FastAPI, HTTPException, UploadFile, File
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.app.database import d1, r2, kv


app = FastAPI()


# D1 Operations
@app.get("/d1/items/{item_id}")
async def read_item(item_id: int):
    query = f"SELECT * FROM items WHERE id = {item_id}"
    result = await d1.get_d1_data(query)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(content=result)


@app.post("/d1/items/")
async def create_item(item_id: int, name: str, description: str):
    query = f"INSERT INTO items (id, name, description) VALUES ({item_id}, '{name}', '{description}')"
    await d1.insert_d1_data(query)
    return {"message": "Item created"}


@app.patch("/d1/items/{item_id}")
async def update_item(item_id: int, name: str = None, description: str = None):
    update_query = "UPDATE items SET "
    if name:
        update_query += f"name = '{name}', "
    if description:
        update_query += f"description = '{description}', "
    update_query = update_query.rstrip(", ")
    update_query += f" WHERE id = {item_id}"
    
    await d1.update_d1_data(update_query)
    return {"message": "Item updated"}


@app.delete("/d1/items/{item_id}")
async def delete_item(item_id: int):
    query = f"DELETE FROM items WHERE id = {item_id}"
    await d1.delete_d1_data(query)
    return {"message": "Item deleted"}


# R2 Operations
@app.post("/r2/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    await r2.upload_to_r2(content, file.filename)
    return {"filename": file.filename, "message": "File uploaded"}


@app.get("/r2/files/{filename}")
async def get_file(filename: str):
    content = await r2.get_from_r2(filename)
    if not content:
        raise HTTPException(status_code=404, detail="File not found")
    return JSONResponse(content={"filename": filename, "content": content.decode("utf-8")})


@app.delete("/r2/files/{filename}")
async def delete_file(filename: str):
    await r2.delete_from_r2(filename)
    return {"message": "File deleted"}


# KV Operations
@app.get("/kv/{key}")
async def kv_get(key: str):
    value = await kv.kv_get(key)
    if not value:
        raise HTTPException(status_code=404, detail="Key not found")
    return JSONResponse(content={"key": key, "value": value})


@app.put("/kv/{key}")
async def kv_put(key: str, value: str):
    await kv.kv_put(key, value)
    return {"message": "Key added/updated"}


@app.patch("/kv/{key}")
async def kv_patch(key: str, value: str):
    await kv.kv_patch(key, value)
    return {"message": "Key patched"}


@app.delete("/kv/{key}")
async def kv_delete(key: str):
    await kv.kv_delete(key)
    return {"message": "Key deleted"}


async def main(request: Request):
    response = await app(request.scope, receive=request.receive, send=request.send)
    return response


def handler(request):
    return asyncio.run(main(request))
