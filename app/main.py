from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
from .transcriber import Transcriber
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Audio Transcription Service",
    description="Сервис для транскрипции аудиофайлов",
    version="1.0.0"
)

transcriber = Transcriber()

SUPPORTED_AUDIO_TYPES = [
    'audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/flac',
    'audio/aac', 'audio/ogg', 'audio/webm'
]

@app.get("/health")
async def health_check():
    """Health check для мониторинга"""
    return {
        "status": "healthy",
        "service": "audio_transcription",
        "model_loaded": transcriber.model is not None
    }

@app.get("/")
async def root():
    return {"message": "Audio Transcription Service is running!"}


@app.get("/Hello!")
async def Hello():
    return {"mesage": "Hello world!"}


@app.get("/How are you")
async def status_check():
    """Проверка здоровья сервиса"""
    return {"status": "I am good", "service": "audio_transcription"}


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Эндпоинт для транскрипции аудиофайлов
    Поддерживаемые форматы: wav, mp3, flac и другие, которые поддерживает Whisper
    """

    if file.content_type not in SUPPORTED_AUDIO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый формат файла. Поддерживаемые форматы: {', '.join(SUPPORTED_AUDIO_TYPES)}"
        )

    file_extension = os.path.splitext(file.filename)[1] or ".tmp"
    temp_filename = f"temp_audio_{uuid.uuid4().hex}{file_extension}"
    temp_path = os.path.join(tempfile.gettempdir(), temp_filename)

    try:
        content = await file.read()
        logger.info(f"Прочитано {len(content)} байт из файла {file.filename}")

        with open(temp_path, 'wb') as f:
            f.write(content)

        logger.info(f"Файл сохранен как: {temp_path}")
        logger.info(f"Полный путь: {os.path.abspath(temp_path)}")

        if not os.path.exists(temp_path):
            raise Exception(f"Не удалось создать временный файл по пути: {temp_path}")

        file_size = os.path.getsize(temp_path)
        logger.info(f"Размер временного файла: {file_size} байт")

        if file_size == 0:
            raise Exception("Временный файл пустой")

        logger.info(f"Начинаем транскрипцию файла: {temp_path}")
        transcription_text = transcriber.transcribe(temp_path)
        logger.info(f"Транскрипция завершена. Получено {len(transcription_text)} символов")
        return JSONResponse({
            "status": "success",
            "text": transcription_text,
            "filename": file.filename,
            "text_length": len(transcription_text)
        })

    except Exception as e:
        logger.error(f"Ошибка при обработке аудио: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обработке аудио: {str(e)}"
        )
    finally:
        if os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
                logger.info(f"Временный файл удален: {temp_path}")
            except Exception as e:
                logger.warning(f"Не удалось удалить временный файл {temp_path}: {e}")


@app.get("/test-transcribe")
async def test_transcribe():
    """Тестовый эндпоинт для проверки работы транскрипции"""
    try:
        audio_file = "noize.mp3"
        #audio_file = "quet.mp3"
        text = transcriber.transcribe(audio_file, language="ru")
        return JSONResponse({
            "status": "success",
            "text": text,
            "filename": "test_audio.wav",
            "message": "Транскрайбер работает (тестовый режим)"
        })
    except Exception as e:
        logger.error(f"Ошибка в тестовом эндпоинте: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Тестовая ошибка: {str(e)}")


# Запуск для разработки
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)