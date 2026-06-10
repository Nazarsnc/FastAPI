from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(
    title="FastAPI Lab 3 - CRUD & Routing",
    description="Синиця Назар, група 32-ІСТ",
    version="1.0.0"
)


app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI CRUD Application! Go to /docs for Swagger UI."}