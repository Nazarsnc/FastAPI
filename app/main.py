from fastapi import FastAPI
# Зміни це: from api.router import api_router
# НА ЦЕ:
from app.api.router import api_router

app = FastAPI(
    title="FastAPI Lab 3 - CRUD & Routing",
    description="Швайковський Денис, група 32-ІСТ",
    version="1.0.0"
)

# Підключаємо всі ендпоінти під префіксом /api/v1
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI CRUD Application! Go to /docs for Swagger UI."}