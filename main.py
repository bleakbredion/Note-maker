import subprocess

import GLOBAL

def run_recording_and_recognition():
    try:
        # Отдельная обработка KeyboardInterrupt на этапе записи
        try:
            subprocess.run([GLOBAL.PYTHON_RECORDING_AND_RECOGNITION, 'recording.py'], check=True)
        except KeyboardInterrupt:
            print("Запись прервана пользователем.")
            return  # Прекратить выполнение распознавания

        subprocess.run([GLOBAL.PYTHON_RECORDING_AND_RECOGNITION, 'recognize.py'], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения: {e}")
    except KeyboardInterrupt:
        print("Операция прервана пользователем.")


def run_realtime_recording_and_recognition():
    try:
        subprocess.run(GLOBAL.PYTHON_RECORDING_AND_RECOGNITION, ['python', 'recording_and_recognition_realtime.py'], check=True)
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
