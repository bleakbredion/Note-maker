import warnings
from deepmultilingualpunctuation import PunctuationModel
from wtpsplit import SaT
from sentence_transformers import SentenceTransformer, util

# Отключение предупреждений
warnings.filterwarnings("ignore", category=UserWarning)

# Инициализация моделей один раз
punct_model = PunctuationModel()
segmenter = SaT("sat-3l")  # Убедитесь, что модель 'sat-3l' установлена и доступна
semantic_model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def make_punctuation(text: str) -> str:
    """
    Восстанавливает знаки препинания в тексте с помощью модели.
    """
    return punct_model.restore_punctuation(text)


def flatten_sentences(sentences):
    """
    Рекурсивно выравнивает вложенные списки предложений в один список.
    """
    flat = []
    for s in sentences:
        if isinstance(s, list):
            flat.extend(flatten_sentences(s))
        elif isinstance(s, dict) and 'sentences' in s:
            flat.extend(flatten_sentences(s['sentences']))
        elif isinstance(s, dict) and 'sentence' in s:
            flat.append(s['sentence'])
        else:
            flat.append(s)
    return flat


def make_semantic_paragraphs(
    sentences: list[str], model: SentenceTransformer, threshold: float = 0.75
) -> list[str]:
    """
    Группирует предложения в абзацы по семантической близости.
    sentences: список уже сегментированных предложений.
    threshold: порог косинусной близости (0-1).
    """
    # Выравниваем и очищаем список
    flat = flatten_sentences(sentences)
    clean_sentences = [str(s).strip() for s in flat if s and len(str(s).strip()) > 2]
    if not clean_sentences:
        return []

    embeddings = model.encode(clean_sentences, convert_to_tensor=True)
    paragraphs = []
    current = [clean_sentences[0]]

    for prev_idx, curr_idx in zip(range(len(clean_sentences) - 1), range(1, len(clean_sentences))):
        sim = util.cos_sim(embeddings[prev_idx], embeddings[curr_idx]).item()
        if sim < threshold:
            paragraphs.append(" ".join(current))
            current = [clean_sentences[curr_idx]]
        else:
            current.append(clean_sentences[curr_idx])
    paragraphs.append(" ".join(current))
    return paragraphs


if __name__ == "__main__":
    # Путь к файлу для чтения
    input_path = "/home/rostislav/python/note maker/Useful files/texts/draft_text.txt"
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except FileNotFoundError:
        raise SystemExit(f"Файл не найден: {input_path}")

    # Шаг 1: восстановление пунктуации
    punctuated = make_punctuation(raw_text)

    # Шаг 2: разбиение на предложения
    sentences = segmenter.split(punctuated, do_paragraph_segmentation=True)
    # Приведение к плоскому списку строк
    if isinstance(sentences, dict) and 'sentences' in sentences:
        sentences = sentences['sentences']
    sentences = flatten_sentences(sentences)

    # Шаг 3: семантическое объединение в абзацы
    paragraphs = make_semantic_paragraphs(sentences, semantic_model)

    # Вывод результатов
    for para in paragraphs:
        print(para)