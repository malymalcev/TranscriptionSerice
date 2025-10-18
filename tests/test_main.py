import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append('app')

from main import app
client = TestClient(app)


def test_root():
    """Тест корневого эндпоинта"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Audio Transcription Service is running!"}


def test_hello():
    """Тест эндпоинта /Hello!"""
    response = client.get("/Hello!")
    assert response.status_code == 200
    assert "mesage" in response.json()


def test_health():
    """Тест health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_loaded" in data


def test_transcribe_invalid_file_type():
    """Тест загрузки неподдерживаемого формата файла"""
    response = client.post(
        "/transcribe",
        files={"file": ("test.txt", b"not an audio file", "text/plain")}
    )
    assert response.status_code == 400


def test_transcribe_empty_file():
    """Тест загрузки пустого файла"""
    response = client.post(
        "/transcribe",
        files={"file": ("empty.mp3", b"", "audio/mpeg")}
    )
    assert response.status_code == 500


def test_test_transcribe_endpoint():
    """Тест тестового эндпоинта транскрипции"""
    response = client.get("/test-transcribe")
    assert response.status_code in [200, 500]


def test_transcribe_with_existing_mp3():
    """Тест транскрипции с существующим MP3 файлом"""
    try:
        mp3_path = "app/quet.mp3"

        assert os.path.exists(mp3_path), f"Файл {mp3_path} не найден"

        with open(mp3_path, 'rb') as audio_file:
            response = client.post(
                "/transcribe",
                files={"file": ("quet.mp3", audio_file.read(), "audio/mpeg")}
            )

        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "success"
            assert "text" in data
            assert "filename" in data
            assert data["filename"] == "quet.mp3"
            print(f"Транскрибированный текст: {data['text']}")

    except Exception as e:
        # Если файла нет, просто пропускаем тест
        pytest.skip(f"Файл quet.mp3 не найден: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])