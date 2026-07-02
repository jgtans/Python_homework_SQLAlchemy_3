from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx

app = FastAPI(title="DummyJSON API Proxy")

# Базовый URL DummyJSON
DUMMYJSON_URL = "https://dummyjson.com"


# Модель для обновления товара (Pydantic)
class ProductUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    # Можно добавить другие поля при необходимости


# Получение всех брендов (категорий)
@app.get("/brands")
async def get_brands():
    """
    Эндпоинт для получения всех брендов (в DummyJSON они представлены как категории).
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DUMMYJSON_URL}/products/categories")

        if response.status_code == 200:
            data = response.json()
            # Вывод данных на экран (в консоль сервера)
            print(f"[GET /brands] Получены бренды: {data}")
            return {"status": "success", "data": data}
        else:
            raise HTTPException(status_code=500, detail="Ошибка при получении брендов из DummyJSON")


# Получение товара по ID
@app.get("/products/{id}/")
async def get_product_by_id(id: int):
    """
    Эндпоинт для получения конкретного товара по его ID.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DUMMYJSON_URL}/products/{id}")

        if response.status_code == 200:
            data = response.json()
            # Вывод данных на экран (в консоль сервера)
            print(f"[GET /products/{id}/] Получен товар: {data}")
            return {"status": "success", "data": data}
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Товар не найден")
        else:
            raise HTTPException(status_code=500, detail="Ошибка при получении товара")


# Обновление товара по ID
@app.put("/products/{id}/update")
async def update_product(id: int, product: ProductUpdate):
    """
    Эндпоинт для обновления данных товара по его ID.
    """
    # Словарь только с теми полями, которые были переданы в запросе
    update_data = product.dict(exclude_unset=True)

    async with httpx.AsyncClient() as client:
        response = await client.put(f"{DUMMYJSON_URL}/products/{id}", json=update_data)

        if response.status_code == 200:
            data = response.json()
            # Вывод данных на экран (в консоль сервера)
            print(f"[PUT /products/{id}/update] Обновлен товар: {data}")
            return {"status": "success", "message": "Товар успешно обновлен", "data": data}
        else:
            raise HTTPException(status_code=500, detail="Ошибка при обновлении товара")