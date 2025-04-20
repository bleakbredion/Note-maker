import warnings
import re
from deepmultilingualpunctuation import PunctuationModel
from sentence_transformers import SentenceTransformer, util

# Отключение предупреждений
warnings.filterwarnings("ignore", category=UserWarning)

# Инициализация моделей один раз
punct_model = PunctuationModel()
semantic_model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def make_punctuation(text: str) -> str:
    """
    Восстанавливает знаки препинания в тексте с помощью модели.
    """
    return punct_model.restore_punctuation(text)


def split_sentences_regex(text: str) -> list[str]:
    """
    Простейшее разбиение текста на предложения по точкам, восклицательным и вопросительным знакам.
    Не разрывает по запятым.
    """
    # Удаляем переводы строк внутри абзаца
    text = text.replace("\n", " ")
    # Разделяем по завершённым предложениям
    sentences = re.split(r'(?<=[\.\!\?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def make_semantic_paragraphs(
    sentences: list[str], model: SentenceTransformer, threshold: float = 0.75, min_sentences: int = 2
) -> list[str]:
    """
    Группирует предложения в абзацы по семантической близости.
    sentences: список предложений, каждое заканчивается точкой, ! или ?.
    threshold: порог косинусной близости (0-1) для разделения.
    min_sentences: минимальное число предложений в абзаце.
    """
    clean = [s for s in sentences if len(s) > 3]
    if not clean:
        return []

    embeddings = model.encode(clean, convert_to_tensor=True)
    paragraphs = []
    current = [clean[0]]

    for i in range(1, len(clean)):
        sim = util.cos_sim(embeddings[i - 1], embeddings[i]).item()
        # Разрываем, только если семантическая дистанция велика и в текущем абзаце уже минимум предложений
        if sim < threshold and len(current) >= min_sentences:
            paragraphs.append(" ".join(current))
            current = [clean[i]]
        else:
            current.append(clean[i])

    # Добавляем последний абзац
    paragraphs.append(" ".join(current))
    return paragraphs


if __name__ == "__main__":
    input_path = "/home/rostislav/python/note maker/Useful files/texts/draft_text.txt"
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except FileNotFoundError:
        raise SystemExit(f"Файл не найден: {input_path}")

    # Восстанавливаем пунктуацию
    punctuated = make_punctuation(raw_text)

    # Разбиваем на предложения по точкам, ?, !
    sentences = split_sentences_regex(punctuated)

    # Семантическое объединение
    paragraphs = make_semantic_paragraphs(sentences, semantic_model, threshold=0.75, min_sentences=2)

    for para in paragraphs:
        print(para)
