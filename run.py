import uvicorn

if __name__ == "__main__":
    # Запускаємо Uvicorn програмно через точку входу Python
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )