from fastapi import FastAPI, testclient
from app.main import app


client = testclient.TestClient(app)

def test_generate_endpoint():
    response = client.post("/generate", data="unique prompt")

    assert response.status_code == 422
    # assert "Failed to communicate with the AI service" in response.text
