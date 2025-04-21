import subprocess

import GLOBAL

def run_recording_and_recognition():
    try:
        # Запуск записи
        record_proc = subprocess.run(
            [GLOBAL.PYTHON_RECORDING_AND_RECOGNITION, '/home/rostislav/python/note maker/Useful files/recording.py', "--no-main"],
            check=False  # Не вызывать исключение при ненулевом коде
        )
        
        # Если запись прервана (код 130) — прекращаем выполнение
        if record_proc.returncode == 130:
            print("Запись прервана. Распознавание отменено.")
            return

        # Если запись завершилась с другой ошибкой
        if record_proc.returncode != 0:
            print(f"Ошибка записи (код {record_proc.returncode})")
            return

        # Распознавание
        subprocess.run([GLOBAL.PYTHON_RECORDING_AND_RECOGNITION, '/home/rostislav/python/note maker/Useful files/recognize.py', "--no-main"], check=True)
        
        # Обработка абзацев
        subprocess.run([GLOBAL.PYTHON_MAKE_PARAGRAPHS, '/home/rostislav/python/note maker/Useful files/make paragraphs.py', "--no-main"], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения: {e}")
    except KeyboardInterrupt:
        print("Операция прервана пользователем.")


def run_realtime_recording_and_recognition():
    try:
        subprocess.run([GLOBAL.PYTHON_RECORDING_AND_RECOGNITION, '/home/rostislav/python/note maker/Useful files/recording and recognition in real time.py', "--no-main"], check=True)
        # Обработка абзацев
        subprocess.run([GLOBAL.PYTHON_MAKE_PARAGRAPHS, '/home/rostislav/python/note maker/Useful files/make paragraphs.py', "--no-main"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения: {e}")
    except KeyboardInterrupt:
        print("Операция прервана пользователем.")



def main() -> int:
    try:
        key = int(input("Выберите режим:\n"
                        "1 — записать и затем распознать\n"
                        "2 — запись и распознавание в реальном времени\n"
                        "Ваш выбор: "))

        match key:
            case 1:
                run_recording_and_recognition()
            case 2:
                run_realtime_recording_and_recognition()
            case _:
                print("Ошибка: Введите 1 или 2.")
                return 1
    except ValueError:
        print("Ошибка: Введите число (1 или 2).")
        return 1

    return 0


if __name__ == "__main__":
    while main() != 0:
        pass
