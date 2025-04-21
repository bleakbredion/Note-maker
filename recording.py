import wave
import sounddevice as sd
import sys
import threading
import numpy as np
from GLOBAL import AUDIO_OUTPUT_PATH

# Настройки аудио
SAMPLE_RATE = 44100  # Частота дискретизации (Гц)
CHANNELS = 1         # Количество каналов (1 = моно)
DTYPE = "int16"      # Формат данных

class Recorder:
    def __init__(self, sample_rate, channels, dtype):
        self.sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self.frames = []
        self.lock = threading.Lock()
        self.stop_flag = threading.Event()

    def callback(self, indata, frames, time, status):
        if status:
            print(f"Статус: {status}")
        with self.lock:
            self.frames.append(indata.copy())
        if self.stop_flag.is_set():
            raise sd.CallbackStop

    def start(self):
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype,
            callback=self.callback
        )
        self.stream.start()

    def stop(self):
        self.stop_flag.set()
        self.stream.stop()
        self.stream.close()

    def save(self, filename):
        with self.lock:
            data = np.concatenate(self.frames, axis=0)
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(np.dtype(self.dtype).itemsize)
            wf.setframerate(self.sample_rate)
            wf.writeframes(data.tobytes())


def record_audio(filename):
    rec = Recorder(SAMPLE_RATE, CHANNELS, DTYPE)
    try:
        print('Запись началась. Введите 0 и нажмите Enter для остановки.')
        rec.start()

        while True:
            user_input = input()
            if user_input.strip() == '0':
                rec.stop()
                break

        rec.save(filename)
        print(f"Запись сохранена в {filename}")
        return True

    except sd.PortAudioError as e:
        print(f"Ошибка доступа к микрофону: {e}")
        return False
    except Exception as e:
        print(f"Ошибка при записи: {e}")
        return False

if __name__ == '__main__':
    success = record_audio(AUDIO_OUTPUT_PATH)
    sys.exit(0 if success else 1)
