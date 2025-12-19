import re
from collections import Counter
from typing import List, Dict, Tuple, Optional


def preprocess_text(text: str) -> List[str]:
    """
    Предобработка текста: очистка и токенизация.
    
    Args:
        text (str): Исходный текст
        
    Returns:
        List[str]: Список слов в нижнем регистре
    """
    if not text or not isinstance(text, str):
        return []
    
    # Приводим к нижнему регистру
    text = text.lower()
    
    # Удаляем все символы, кроме букв, цифр и пробелов
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Заменяем множественные пробелы на одинарные
    text = re.sub(r'\s+', ' ', text)
    
    # Разбиваем на слова
    words = text.strip().split()
    
    return words


def count_words(text: str) -> int:
    """
    Подсчёт количества слов в тексте.
    
    Args:
        text (str): Исходный текст
        
    Returns:
        int: Количество слов
    """
    words = preprocess_text(text)
    return len(words)


def count_unique_words(text: str) -> int:
    """
    Подсчёт количества уникальных слов в тексте.
    
    Args:
        text (str): Исходный текст
        
    Returns:
        int: Количество уникальных слов
    """
    words = preprocess_text(text)
    unique_words = set(words)
    return len(unique_words)


def calculate_ttr(text: str) -> float:
    """
    Вычисление коэффициента Type-Token Ratio.
    
    TTR = (количество уникальных слов) / (общее количество слов)
    
    Args:
        text (str): Исходный текст
        
    Returns:
        float: Коэффициент TTR (от 0 до 1)
    """
    total_words = count_words(text)
    unique_words = count_unique_words(text)
    
    # Защита от деления на ноль
    if total_words == 0:
        return 0.0
    
    return round(unique_words / total_words, 4)


def count_lines(text: str) -> int:
    """
    Подсчёт количества строк в тексте.
    
    Args:
        text (str): Исходный текст
        
    Returns:
        int: Количество строк
    """
    if not text:
        return 0
    
    # Разделяем текст на строки и удаляем пустые строки
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return len(lines)


def get_most_common_words(text: str, n: int = 10) -> List[Tuple[str, int]]:
    """
    Получение топ-N самых частотных слов в тексте.
    
    Args:
        text (str): Исходный текст
        n (int): Количество слов для возврата
        
    Returns:
        List[Tuple[str, int]]: Список кортежей (слово, частота)
    """
    words = preprocess_text(text)
    
    if not words:
        return []
    
    # Подсчитываем частоту слов
    word_counts = Counter(words)
    
    # Возвращаем N самых частотных слов
    return word_counts.most_common(n)


def average_word_length(text: str) -> float:
    """
    Вычисление средней длины слова в тексте.
    
    Args:
        text (str): Исходный текст
        
    Returns:
        float: Средняя длина слова
    """
    words = preprocess_text(text)
    
    if not words:
        return 0.0
    
    total_length = sum(len(word) for word in words)
    return round(total_length / len(words), 2)


def find_longest_word(text: str) -> str:
    """
    Нахождение самого длинного слова в тексте.
    
    Args:
        text (str): Исходный текст
        
    Returns:
        str: Самое длинное слово
    """
    words = preprocess_text(text)
    
    if not words:
        return ""
    
    # Находим слово с максимальной длиной
    return max(words, key=len)


def calculate_lexical_density(text: str) -> float:
    """
    Вычисление лексической плотности текста.
    
    Лексическая плотность = (количество знаменательных слов) / (общее количество слов)
    В упрощенной версии считаем знаменательными слова длиной более 3 символов.
    
    Args:
        text (str): Исходный текст
        
    Returns:
        float: Лексическая плотность (от 0 до 1)
    """
    words = preprocess_text(text)
    
    if not words:
        return 0.0
    
    # Считаем знаменательные слова (длиной более 3 символов)
    lexical_words = [word for word in words if len(word) > 3]
    
    # Защита от деления на ноль
    if not words:
        return 0.0
    
    return round(len(lexical_words) / len(words), 4)


def calculate_sentence_count(text: str) -> int:
    """
    Подсчет количества предложений в тексте.
    
    Args:
        text (str): Исходный текст
        
    Returns:
        int: Количество предложений
    """
    if not text:
        return 0
    
    # Упрощенный подсчет предложений
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return len(sentences)


def analyze_text_readability(text: str) -> Dict[str, float]:
    """
    Анализ удобочитаемости текста (упрощенный).
    
    Args:
        text (str): Исходный текст
        
    Returns:
        Dict[str, float]: Показатели удобочитаемости
    """
    if not text:
        return {"readability_score": 0.0}
    
    words = preprocess_text(text)
    sentences = calculate_sentence_count(text)
    
    if not words or sentences == 0:
        return {"readability_score": 0.0}
    
    # Упрощенная оценка: чем меньше слов в предложении, тем проще текст
    words_per_sentence = len(words) / sentences
    
    # Нормализуем оценку (0-100)
    readability_score = max(0, min(100, 100 - (words_per_sentence - 10) * 2))
    
    return {
        "readability_score": round(readability_score, 2),
        "words_per_sentence": round(words_per_sentence, 2),
        "sentences": sentences
    }