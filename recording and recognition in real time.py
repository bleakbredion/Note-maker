
import pyaudio
import whisper
import wave
import tempfile

# Параметры аудио
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 4  # Длина фрагмента
OVERLAP_SECONDS = 0.5  # Перекрытие

model = whisper.load_model("base")

def record_and_transcribe():
    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(format=FORMAT, channels=CHANNELS,
                                  rate=RATE, input=True,
                                  frames_per_buffer=CHUNK)

    print("Запись началась... (нажмите Ctrl+C для остановки)")

    buffer = []  # Храним последние N секунд для перекрытия

    try:
        while True:
            frames = []

            for _ in range(int(RATE / CHUNK * (RECORD_SECONDS - OVERLAP_SECONDS))):
                data = stream.read(CHUNK)
                frames.append(data)

            # Добавляем часть из предыдущего буфера (перекрытие)
            frames = buffer + frames

            # Запоминаем последние OVERLAP_SECONDS для следующего фрагмента
            #buffer = frames[-int(RATE / CHUNK * OVERLAP_SECONDS):]
            buffer = frames[-int(len(frames) * OVERLAP_SECONDS / RECORD_SECONDS):]

            with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as tmpfile:
                wf = wave.open(tmpfile.name, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio_interface.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()

                result = model.transcribe(tmpfile.name, language="ru")
                print("Распознанный текст:", result["text"])

    except KeyboardInterrupt:
        print("\nОстановка записи...")
        stream.stop_stream()
        stream.close()
        audio_interface.terminate()

if __name__ == "__main__":
    record_and_transcribe()
