import whisper
import logging
import os

logger = logging.getLogger(__name__)

class Transcriber:
    def __init__(self, model_size="medium"):
        """
        Простой транскрибер на основе Whisper
        """
        self.model_size = model_size
        self.model = None
        self._load_model()

    def _load_model(self):
        """Загрузка модели в память"""
        try:
            logger.info(f"Загружаем модель {self.model_size}...")
            self.model = whisper.load_model(self.model_size)
            logger.info("Модель загружена!")
        except Exception as e:
            logger.error(f"Ошибка загрузки модели: {e}")
            raise

    def transcribe(self, audio_path, language=None):
        """
        Транскрибирует аудиофайл в текст
        """
        if self.model is None:
            self._load_model()

        try:
            logger.info(f"Начало транскрибации файла: {audio_path}")

            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Файл не существует: {audio_path}")

            file_size = os.path.getsize(audio_path)
            logger.info(f"Размр файла: {file_size} байт")

            if file_size == 0:
                raise ValueError("Файл пустой")

            result = self.model.transcribe(audio_path,language=language)
            text = result["text"].strip()

            logger.info(f"Транскрибвция завершена. Длина текста: {len(text)} символов")
            return text

        except Exception as e:
            logger.error(f"Ошибка транскрибации: {e}")
            raise