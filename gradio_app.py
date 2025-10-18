import gradio as gr
import requests
import os

API_URL = os.getenv("API_URL", "http://transcription-service:8000")

# API_URL = os.getenv("API_URL", "http://localhost:8000")

def transcribe_audio(audio_file):
    try:
        if not audio_file or not os.path.exists(audio_file):
            return "❌ Файл не найден"

        with open(audio_file, 'rb') as f:
            files = {'file': (os.path.basename(audio_file), f, 'audio/mpeg')}
            response = requests.post(f"{API_URL}/transcribe", files=files)

        if response.status_code == 200:
            result = response.json()
            text = result.get('text', '')
            filename = result.get('filename', 'unknown')
            length = result.get('text_length', 0)
            return f"""✅ **Транскрипция завершена!**

📄 **Файл:** {filename}
📝 **Текст:** {text}
📊 **Количество символов:** {length}"""
        else:
            return "❌ Ошибка транскрипции"

    except:
        return "❌ Ошибка подключения к сервису"


def health_check():
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            return "🟢 Сервис работает"
        return "🔴 Сервис недоступен"
    except:
        return "🔴 Сервис не отвечает"


with gr.Blocks(title="Транскрипция аудио") as demo:
    gr.Markdown("# 🎙️ Транскрипция аудио в текст")

    with gr.Accordion("📋 Правила использования", open=False):
        gr.Markdown("""
        **Как пользоваться:**
        1. Загрузите аудиофайл или запишите голос
        2. Нажмите кнопку «Транскрибировать»
        3. Дождитесь результата

        **Поддерживаемые форматы:** MP3, WAV, FLAC, M4A, OGG
        **Максимальный размер:** 25MB

        ⚠️ **Важно:** Убедитесь, что сервис транскрипции запущен на localhost:8000
        """)

    with gr.Row():
        status = gr.Textbox(label="Статус", value="Проверка...")
        gr.Button("🔄 Обновить").click(health_check, outputs=status)

    audio = gr.Audio(sources=["upload", "microphone"], type="filepath")
    btn = gr.Button("🎯 Транскрибировать")
    output = gr.Textbox(
        label="Результат транскрипции",
        placeholder="Здесь появится преобразованный текст...",
        lines=8,
        show_copy_button=True
    )

    btn.click(transcribe_audio, inputs=audio, outputs=output)
    demo.load(health_check, outputs=status)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )

# if __name__ == "__main__":
#     demo.launch(
#         server_name="0.0.0.0",  # ← ДОБАВИТЬ ЭТУ СТРОКУ
#         server_port=7860,
#         share=True
#     )

# if __name__ == "__main__":
#     demo.launch(share=True)