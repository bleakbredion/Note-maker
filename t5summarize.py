from pathlib import Path
from transformers import pipeline
from GLOBAL import RECOGNIZED_TEXTS
# Загрузка модели для суммаризации
summarizer = pipeline("summarization", model="/home/rostislav/python/speech recognition/models/dowload t5summarizer")

# Текст, который нужно суммаризировать
text_path = Path(RECOGNIZED_TEXTS[0])
#text_path = Path("/home/rostislav/python/speech recognition/Яна монолог whisper-large-v3-turbo-russian try 2.txt")

with open(text_path, mode="r", encoding="utf-8") as file:
    text = file.    read()

# Суммаризация текста
summary = summarizer(text, max_length=800, min_length=50, do_sample=False)

print(summary[0]['summary_text'])
