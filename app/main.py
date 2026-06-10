from fastapi import FastAPI

from app.api.router import api_router


app = FastAPI(title="FastAPI Lab 5", version="1.0.0")


app.include_router(api_router)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is running"}