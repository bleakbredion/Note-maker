from GLOBAL import DRAFT_TEXT_PATH
import pyaudio
import whisper
import wave
import io
import sys
import warnings
import numpy as np

# Параметры записи
CHUNK = 512                  # Уменьшен для снижения задержки
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 4
OVERLAP_SECONDS = 1.5        # Увеличенное перекрытие
OUTPUT_FILE = DRAFT_TEXT_PATH

# Инициализация модели (рекомендуется 'small' для русского)
model = whisper.load_model("small")

def record_and_transcribe():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("Запись началась... (Ctrl+C для остановки)")
    buffer = []

    try:
        while True:
            # Расчет чанков для основного сегмента и перекрытия
            main_frames = int(RATE / CHUNK * (RECORD_SECONDS - OVERLAP_SECONDS))
            overlap_frames = int(RATE / CHUNK * OVERLAP_SECONDS)
            
            # Запись основного сегмента
            frames = []
            for _ in range(main_frames):
                frames.append(stream.read(CHUNK))
            
            # Добавление буфера предыдущего перекрытия
            frames = buffer + frames
            buffer = frames[-overlap_frames:]  # Сохраняем перекрытие

            # Создание WAV в памяти (без временных файлов)
            with io.BytesIO() as wav_buffer:
                with wave.open(wav_buffer, 'wb') as wf:
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(audio.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                
                # Транскрипция
                wav_buffer.seek(0)
                with wave.open(wav_buffer, 'rb') as wf:
                    n_samples = wf.getnframes()
                    audio_data = wf.readframes(n_samples)
                    audio_np = np.frombuffer(audio_data, dtype=np.int16)
                    audio_np = audio_np.astype(np.float32) / 32768.0  # Нормализация

                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    result = model.transcribe(
                        audio_np,
                        language="ru",
                        fp16=False  # Уберите, если используете GPU
                    )

                # Запись результата
                text = result["text"].strip()
                if text:
                    try:
                        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
                            f.write(text + ' ')
                        print("Распознано:", text)
                    except Exception as e:
                        print(f"Ошибка записи: {e}")

    except KeyboardInterrupt:
        print("\nЗавершение записи...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

# Очистка файла перед запуском
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write('')

if __name__ == "__main__" and "--no-main" not in sys.argv:
    record_and_transcribe()

else:
    record_and_transcribe()