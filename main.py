import subprocess

def recording_and_recognize():
    try:
        subprocess.run(['python', 'recording.py'], check=True)
    except KeyboardInterrupt:
        pass
    subprocess.run(['python', 'recognize.py'])


def recording_and_recognize_in_real_time():
    try:
        subprocess.run(['python', 'recording and recognition in real time.py'], check=True)
    except KeyboardInterrupt:
        pass

def main() -> int:
    try:
        key = int(input())

        match key:
            case 1:
                recording_and_recognize()
            case 2:
                recording_and_recognize_in_real_time()
            case _:
                print("Нажмите 1 или 2:")
                return 1
    except ValueError:
        print("Ошибка: Введите число 1 или 2")
        return 1

    return 0


print("Записать и после распознать (нажмите 1) или записывать и распознавать в реальном времени (нажмите 2):")

while main() != 0:
    pass
