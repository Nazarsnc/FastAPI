# fastapi_template/main.py
from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Template",
    description="Базовий шаблон проєкту на FastAPI",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "working", "message": "Welcome to FastAPI Template"}