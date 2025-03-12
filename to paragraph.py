from nltk.tokenize import sent_tokenize

class TextProcessor:
    def __init__(self, sentences_per_paragraph=3):
        self.sentences = []
        self.sentences_per_paragraph = sentences_per_paragraph

    def add_sentence(self, text):
        new_sentences = sent_tokenize(text, language="russian")
        self.sentences.extend(new_sentences)

        # Если накоплено достаточно предложений, создаем новый абзац
        if len(self.sentences) >= self.sentences_per_paragraph:
            paragraph = " ".join(self.sentences)
            self.sentences = []  # Очищаем буфер предложений
            return paragraph
        return None  # Возвращает None, если абзац еще не сформирован

if __name__ == "__main__":
    processor = TextProcessor(sentences_per_paragraph=3)

    sample_texts = [
        "Это первое предложение. Второе предложение тоже здесь.",
        "Третье предложение завершает абзац. А это новое предложение.",
        "Продолжаем. Следующий абзац начнется после этого."
    ]

    for text in sample_texts:
        paragraph = processor.add_sentence(text)
        if paragraph:
            print("Сформирован абзац:", paragraph)
