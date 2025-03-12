import sounddevice as sd
import wave
import sys

FILENAME = "output.wav"
RATE = 44100
CHANNELS = 1
DATATYPE = "int16"
CHUNK_DURATION = 1  # Длина записываемого фрагмента в секундах

with wave.open(FILENAME, "wb") as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # 16 бит = 2 байта
    wf.setframerate(RATE)

    print("Начало записи (для остановки нажмите CTRL+C)")

    try:
        while True:
            audio = sd.rec(int(CHUNK_DURATION * RATE), samplerate=RATE, channels=CHANNELS, dtype=DATATYPE)
            sd.wait()
            wf.writeframes(audio.tobytes())

    except KeyboardInterrupt:
        print("\nОстановка записи")
        sys.exit(0)  # Корректный выход без ошибки
