#import speech_recognition as speech_rg
import whisper

INFILENAME = 'output.wav'
#INFILENAME = "/home/rostislav/python/speech recognition/Useful files/Яна монолог.wav"

def recognize_by_google():

    # Распознавание речи
    r = speech_rg.Recognizer()

    # Открываем WAV файл для распознавания
    with speech_rg.AudioFile(INFILENAME) as audio_file:
        r.adjust_for_ambient_noise(audio_file)  # Подстроиться под фоновый шум
        content = r.record(audio_file)  # Считываем содержимое
        try:
            # Распознаем речь
            print("Start recognized")
            recognized_text = r.recognize_google(content, language="ru-RU")
            print("Recognized text:\n", recognized_text)
        except speech_rg.UnknownValueError:
            print("Google Speech Recognition не смог распознать аудио")
        except speech_rg.RequestError as e:
            print(f"Не удалось запросить результаты от Google Speech Recognition; {e}")

def recognize_by_whisper(model_name="base"):
    print("Распознание начато")
    model = whisper.load_model(model_name)
    result = model.transcribe(INFILENAME, language="ru")
    print("Распознанный текст:", result["text"])

recognize_by_whisper()
#recognize_by_google()
