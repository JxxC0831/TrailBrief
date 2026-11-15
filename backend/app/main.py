from fastapi import FastAPI
from app.api import weather

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(weather.router)
