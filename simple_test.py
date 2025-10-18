import sys
import os

sys.path.append('app')

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_basic():
    print("=== Testing basic endpoints ===")

    # Test root
    response = client.get("/")
    print(f"Root: {response.status_code} - {response.json()}")

    # Test health
    response = client.get("/health")
    print(f"Health: {response.status_code} - {response.json()}")

    # Test invalid file
    response = client.post(
        "/transcribe",
        files={"file": ("test.txt", b"not audio", "text/plain")}
    )
    print(f"Invalid file: {response.status_code}")

    print("=== Basic tests completed ===")


if __name__ == "__main__":
    test_basic()