import pytest
from fastapi.testclient import TestClient


def test_ping(client: TestClient):
    response = client.post('/ping')
    assert response.status_code == 200
    assert response.json() == 'pong'
