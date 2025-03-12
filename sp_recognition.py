from pathlib import Path
from transformers import pipeline

# Загружаем пайплайн для распознавания речи
model_path = Path("/home/rostislav/python/speech recognition/models/download whisper-small")
pipe = pipeline("automatic-speech-recognition",
                model=model_path.as_posix())

# Распознаем аудиофайл
def transcribe(audio_path):
    result = pipe(audio_path, return_timestamps=True, chunk_length_s=30)
    return result["text"]

# Пример использования
audiofile_path = Path("/home/rostislav/python/speech recognition/Яна монолог.wav")   # Укажи путь к своему файлу
audio_file = audiofile_path.as_posix()
recognized_text = transcribe(audio_file)
print("Распознанный текст:", recognized_text)
