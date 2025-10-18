# Audio Transcription Service
Сервис для транскрибирования аудиофайлов в текст с использованием модели Whisper и FastAPI.



## Структура проекта:

transcription_project/
├── 📁 app/                         # Основное приложение
│   ├── __init__.py
│   ├── main.py                     # FastAPI приложение и эндпоинты
│   ├── models.py                   # Модели для API
│   ├── transcriber.py              # Логика транскрибирования с Whisper
│   ├── noize.mp3                   # Тестовый зашумленный аудиофайл
│   └── quet.mp3                    # Тестовый аудиофайл
├── 📁 tests/                       # Тесты
│   ├── __init__.py
│   ├── test_main.py                # Основные тесты API
│   └── .pytest_cache/
├── 📄 Dockerfile                   # Конфигурация Docker контейнера
├── 📄 Dockerfile.gradio            # Конфигурация Docker для Gradio
├── 📄 .dockerignore 
├── 📄 docker-compose.yml           # Docker Compose для полного развертывания
├── 📄 requirements.txt             # Общие зависимости для локального запуска
├── 📄 requirements-api.txt         # Зависимости API для Docker
├── 📄 requirements-gradio.txt      # Зависимости Gradio для Docker
├── 📄 simple_test.py               # Простой тестовый скрипт
├── 📄 gradio_test.py               # Тестовый скрипт для Gradio интерфейса
├── 📄 gradio_app.py                # Web интерфейс на Gradio
└── 📄 README.md                    # Документация

Предварительные требования:
- Python 3.9+
- Docker и Docker Compose (для контейнеризации)
- 2GB+ свободной оперативной памяти
- ~4GB свободного места на диске (для моделей Whisper и интерфейса Gradio)


## Быстрый запуск

1. Распакуйте архив
2. Запустите: `docker-compose up --build`
3. Откройте: http://localhost:7860

## Требования
- Docker 20.10+
- Docker Compose 2.0+
- 4GB свободной памяти


## Запуск программы
В данной реализации есть возможность запустить Web-интерфейс на публичной ссылке и поделиться ей с кем-то. Для
этого необходимо:
1. Перейти в файл gradio_app.py
2. В самом низу файла найти строчки: if __name__ == "__main__":
3. Там вы увидите 2 варианта:
- если вы хотите запустить локальную ссылку, то оставляйте share=False
- если хотите запустить публичную ссылку, то поставть share=True

Локальный запуск (без Docker)
1. Установите зависимости:
pip install -r requirements.txt
2. Запустите сервис
cd app
python main.py
3. Сервис будет доступен по адресу: http://localhost:8000

Запуск в Docker
1. Соберите и запустите контейнер
docker-compose up --build
2. Сервисы будут доступны по адресам:
- API: http://localhost:8000
- Web интерфейс: http://localhost:7860
Если запуск на публичной ссылке, то она будет указана в терминале.



## API и документация
После запуска сервиса документация API доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Основные эндпоинты
- GET /
Описание: Статус сервиса
Ответ: 
{
"message": "Audio Transcription Service is running!"
}
- GET /health
Описание: Health check для мониторинга
Ответ:
{
  "status": "healthy",
  "service": "audio_transcription", 
  "model_loaded": true
}
- GET /HELLO!
Описание: Стандартный тестовый запрос
Ответ:
{
  "mesage": "Hello world!"
}
- GET /How are you
Описание: Еще один подобный тестовый запрос
Ответ:
{
  "status": "I am good",
  "service": "audio_transcription"
}
- POST /transcribe
Описание: Транскрибирование аудиофайла
Поддерживаемые форматы: WAV, MP3, FLAC, AAC, OGG, WEBM
Параметры:
file: Аудиофайл для транскрибирования
Ответ:
{
  "status": "success",
  "text": "транскрибированный текст",
  "filename": "original_filename.mp3",
  "text_length": 150
}
- GET /test-transcribe
Описание: Тестовый эндпоинт для проверки работы
Ответ: Тестовый результат транскрибирования



## Тестирование

Запуск тестов:
- Все тесты
pytest tests/ -v

- Конкретный тестовый файл
pytest tests/test_main.py -v

- Простой тест
python simple_test.py

Покрытие тестами:
- Тесты корневых эндпоинтов
- Тесты health check
- Тесты валидации файлов
- Тесты обработки ошибок
- Интеграционные тесты с реальными аудиофайлами



## Технологии
- **FastAPI** - современный Python фреймворк для API
- **Whisper** - модель транскрибирования от OpenAI
- **Gradio** - фреймворк для простых веб-интерфейсов
- **Docker** - контейнеризация приложения
- **Pydantic** - валидация данных
- **Pytest** - тестирование
- **Uvicorn** - ASGI сервер



## Модели Whisper
Сервис поддерживает различные размеры моделей:

- base (~74MB) - быстрая, умеренная точность
- small (~244MB) - баланс скорости и точности
- medium (~1.5GB) - высокая точность (Мне кажется этого достаточно для большинства задач)
- large (~3.1GB) - максимальная точность (Излишняя точность по моему мнению)



## Работа с Docker

- Запуск всех сервисов
docker-compose up --build
- Запуск в фоновом режиме
docker-compose up -d
- Просмотр логов
docker-compose logs -f transcription-service
docker-compose logs -f gradio-demo
- Остановка сервиса
docker-compose down
- Индивидуальные контейнеры
Только API сервис
docker build -t transcription-service .
docker run -p 8000:8000 transcription-service
Только Gradio демо
docker build -f Dockerfile.gradio -t gradio-demo .
docker run -p 7860:7860 gradio-demo



## Поиск и устранение неисправностей

- Проблема: Медленная загрузка модели
Решение: В файле transcriber.py при инициализации обьекта transcriber в параметрах изменить размер модели.
Через переменную окружения model_size="medium" (по умолчанию экземпляр класса создается с моделью размера medium).
Используйте меньшую модель (base или small) .

- Проблема: Ошибка памяти
Решение: Увеличьте лимиты памяти в Docker или используйте меньшую модель Whisper.

- Проблема: Файл не поддерживается
Решение: Проверьте, что файл в поддерживаемом формате (MP3, WAV, FLAC и т.д.).
- Проблема: Модель не загружается
Решение:
docker-compose down -v
docker-compose up --build

- Проблема: Программа выдает ошибку при запуске.
Решение: Мне не удалось решить проблему с точкой в файле main.py. Если вы запускаете программу через Docker,
чтобы не вылезла ошибка при сборке нужно поставить точку в пятой строке и после этого включать сборку:
from .transcriber import Transcriber
Если программа запускается через IDE, то точку нужно убрать:
from transcriber import Transcriber



## Производительность
- Время транскрибирования: зависит от длины аудио и размера модели
- Память: 1-4GB в зависимости от модели Whisper
- Поддерживает параллельные запросы через ASGI
- Кеширование: Модели кешируются в Docker volume для быстрой перезагрузки



## Масштабирование
Добавление новых эндпоинтов
- Добавьте эндпоинт в app/main.py
- Добавьте соответствующие модели в app/models.py
- Напишите тесты в tests/test_main.py

