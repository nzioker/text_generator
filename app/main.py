from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.utils.db_init import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"Status": "Running"}

@app.get("/")
def home():
    return "This is home."


@app.post("/generate")
def generate():
    return "Generate text"

@app.get("/history")
def history():
    return "What has been generated and stored in the db"
