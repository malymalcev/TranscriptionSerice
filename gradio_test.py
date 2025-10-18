"""
Тест для Gradio приложения
"""

import requests
import time


def test_gradio_connection():
    """Тест подключения к Gradio интерфейсу"""
    try:
        response = requests.get("http://localhost:7860", timeout=10)
        print(f"✅ Gradio интерфейс доступен (статус: {response.status_code})")
        return True
    except Exception as e:
        print(f"❌ Gradio интерфейс недоступен: {e}")
        return False


def test_api_connection():
    """Тест подключения к API"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ API сервис доступен (статус: {response.status_code})")
        return True
    except Exception as e:
        print(f"❌ API сервис недоступен: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Тестирование демо-стенда...")

    time.sleep(5)

    api_ok = test_api_connection()
    gradio_ok = test_gradio_connection()

    if api_ok and gradio_ok:
        print("\n🎉 Все сервисы работают корректно!")
        print("🌐 Gradio демо доступно по адресу: http://localhost:7860")
        print("🔗 API документация: http://localhost:8000/docs")
    else:
        print("\n⚠️ Некоторые сервисы требуют внимания")