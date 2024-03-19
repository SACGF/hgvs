import os
import sys
from fastapi import Path
import pytest
import logging
from fastapi.testclient import TestClient

current_dir = os.path.dirname(os.path.abspath(__file__))
target_folder_path = os.path.join(current_dir, "..")
sys.path.append(target_folder_path)

logger = logging.getLogger(__name__)

class TestHealth:   
    def test_home_returns_success(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_api_is_alive(self, client):
        response = client.get("/health/alive")
        assert response.status_code == 200
        assert response.json() == {"status": "alive"}

    def test_api_is_ready(self, client):
        response = client.get("/health/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}
