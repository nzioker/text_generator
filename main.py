from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return "This is home."


@app.post("/generate")
def generate():
    return "Generate text"

@app.get("/history")
def history():
    return "What has been generated and stored in the db"

