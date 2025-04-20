from GLOBAL import AUDIO_OUTPUT_PATH
import sounddevice as sd
import wave
import sys


DATATYPE = "int16"
CHANNELS = 1
RATE = 16000

CHUNK_DURATION = 1  # Длина записываемого фрагмента в секундах


def recording_loop(wf):
    try:
        # Проверка доступа к микрофону
        test_audio = sd.rec(int(0.1 * RATE), samplerate=RATE, channels=CHANNELS, dtype=DATATYPE)
        sd.wait()
    except sd.PortAudioError as e:
        print(f"Ошибка доступа к микрофону: {e}")
        sys.exit(1)


    try:
        while True:
            # Проверка ввода (неблокирующий ввод)
            user_input = input("Нажмите 0 для остановки...\n").strip()
            if user_input == '0':
                print("Остановка по запросу пользователя.")
                return True  # Флаг для корректного завершения

            # Запись
            audio = sd.rec(int(CHUNK_DURATION * RATE), samplerate=RATE, channels=CHANNELS, dtype=DATATYPE)
            sd.wait()
            wf.writeframes(audio.tobytes())

    except KeyboardInterrupt:
        print("\nОстановка записи (CTRL+C)")
        return False


def record(FILENAME=AUDIO_OUTPUT_PATH):
    with wave.open(FILENAME, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16 бит = 2 байта
        wf.setframerate(RATE)

        # Можно вернуть если разобраться с остановкой main при нажатии CTRL+C
        #print("Начало записи (для остановки нажмите CTRL+C)")

        if recording_loop(wf):
            print("Запись завершена.")
        else:
            sys.exit(130)  # Заверщение с ошибкой


if __name__ == "__main__" and "--no-main" not in sys.argv:
    record(FILENAME=AUDIO_OUTPUT_PATH)

else:
    record(FILENAME=AUDIO_OUTPUT_PATH)