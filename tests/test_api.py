from unittest.mock import patch

import httpx
from groq import APIError
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_unexpected_error():
    with patch(
        "app.main.generate_response",
        side_effect=Exception("Internal provider details"),
    ):
        response = client.post(
            "/ai/chat",
            json={"message": "Find me a mouse"},
        )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "An unexpected error occurred. Please try again."
    }
    assert "Internal provider details" not in response.text



def test_groq_api_failure():
    groq_error = APIError(
        "Groq provider failed",
        httpx.Request("POST", "https://api.groq.com"),
        body=None,
    )

    with patch(
        "app.main.generate_response",
        side_effect=groq_error,
    ):
        response = client.post(
            "/ai/chat",
            json={"message": "Find me a mouse"},
        )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "The AI service is temporarily unavailable. Please try again."
    }
    assert "Groq provider failed" not in response.text


def test_empty_message_rejected():
    response = client.post(
        "/ai/chat",
        json={"message": ""},
    )

    assert response.status_code == 422
