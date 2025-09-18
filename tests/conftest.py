import sys
import pathlib
import pytest
from fastapi.testclient import TestClient

# Ensure repo root is on sys.path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from api.main import app  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    """Shared FastAPI test client."""
    return TestClient(app)
