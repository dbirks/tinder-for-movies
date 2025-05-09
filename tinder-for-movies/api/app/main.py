from fastapi import FastAPI
from .db import get_db

app = FastAPI(title="Tinder for Movies API")

@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

@app.get("/health")
def health():
    # Optionally check DB connection here
    return {"status": "ok"}
