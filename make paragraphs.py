from GLOBAL import DRAFT_TEXT_PATH, STRUCTURED_TEXT_PATH
import warnings
import re
from deepmultilingualpunctuation import PunctuationModel
from sentence_transformers import SentenceTransformer, util
import sys

# Отключение предупреждений
warnings.filterwarnings("ignore", category=UserWarning)

# Инициализация моделей один раз
punct_model = PunctuationModel()
semantic_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


def make_punctuation(text: str) -> str:
    """
    Восстанавливает знаки препинания в тексте с помощью модели.
    """
    if not text.strip():
        return ""
    return punct_model.restore_punctuation(text)


def split_sentences_regex(text: str) -> list[str]:
    """
    Разбиение текста на предложения по ., !, ?.
    Переводы строк удаляются. Начало каждого предложения приводится к заглавной букве.
    """
    text = text.replace("\n", " ")
    sentences = re.split(r'(?<=[\.\!\?])\s+', text)
    
    result = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        # Преобразуем первую букву в заглавную, оставляя остальное без изменений
        s = s[0].upper() + s[1:] if s else s
        result.append(s)
    
    return result


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



def make_paragraphs(
    input_path=DRAFT_TEXT_PATH, 
    output_path=STRUCTURED_TEXT_PATH
    ):
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

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(paragraphs))


if __name__ == "__main__" and "--no-main" not in sys.argv:
    #INPUT_PATH = "/home/rostislav/python/note maker/Useful files/texts/draft_text.txt"
    INPUT_PATH = DRAFT_TEXT_PATH
    OUTPUT_PATH = STRUCTURED_TEXT_PATH
    make_paragraphs(INPUT_PATH, OUTPUT_PATH)

    print("Структурированный текст сохранен в:", OUTPUT_PATH)

    for para in paragraphs:
        print(para)

else:
    make_paragraphs()
    print("Структурированный текст сохранен в:", STRUCTURED_TEXT_PATH)