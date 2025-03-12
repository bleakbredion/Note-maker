import subprocess
import os

def convert_to_wav(input_file, output_file="output.wav", sample_rate=16000, channels=1):
    """
    Конвертирует аудиофайл в WAV с заданными параметрами.

    :param input_file: Путь к входному файлу (MP3, AAC, OGG и т. д.).
    :param output_file: Имя выходного файла (WAV).
    :param sample_rate: Частота дискретизации (по умолчанию 16 кГц).
    :param channels: Количество каналов (1 = моно, 2 = стерео).
    """
    if not os.path.exists(input_file):
        print(f"Ошибка: Файл {input_file} не найден!")
        return False

    command = [
        "ffmpeg", "-y",  # -y перезаписывает файл без запроса
        "-i", input_file,  # Входной файл
        "-ac", str(channels),  # Количество каналов (1 = моно)
        "-ar", str(sample_rate),  # Частота дискретизации
        "-sample_fmt", "s16",  # Формат сэмплов (16 бит)
        output_file  # Выходной WAV-файл
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Конвертация завершена: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print("Ошибка при конвертации:", e)
        return False

# Пример использования
input_mp3 = "input.mp3"  # Укажи свой файл
convert_to_wav(input_mp3, "converted.wav")
