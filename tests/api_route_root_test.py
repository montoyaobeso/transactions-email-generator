from unittest import TestCase

from fastapi.testclient import TestClient

from src.app.main import app


class TestRootEntrypoint(TestCase):
    client = TestClient(app)

    def test_root_endpoint(self):
        # Arrange
        expected_response = {
            "message": "Welcome to transactions email generator API.",
        }

        # Act
        response = self.client.get("/")

        # Assert
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.json(), expected_response)
