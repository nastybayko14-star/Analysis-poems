import os
import sys
import time
from datetime import datetime
from typing import List, Dict, Any

import file_utils
import text_utils


def analyze_single_text(filepath: str, filename: str = None) -> Dict[str, Any]:
    """
    Анализирует один текстовый файл.
    
    Args:
        filepath (str): Путь к файлу
        filename (str, optional): Имя файла (если None, берется из filepath)
        
    Returns:
        Dict[str, Any]: Словарь с результатами анализа
    """
    if filename is None:
        filename = os.path.basename(filepath)
    
    print(f"  📄 Анализирую: {filename}")
    
    # Читаем содержимое файла
    content = file_utils.read_text_file(filepath)
    
    if content is None:
        print(f"    ⚠️ Не удалось прочитать файл")
        return {}
    
    # Выполняем анализ текста
    results = {
        "filename": filename,
        "word_count": text_utils.count_words(content),
        "unique_words": text_utils.count_unique_words(content),
        "ttr": text_utils.calculate_ttr(content),
        "line_count": text_utils.count_lines(content),
        "avg_word_length": text_utils.average_word_length(content),
        "longest_word": text_utils.find_longest_word(content),
        "lexical_density": text_utils.calculate_lexical_density(content),
        "file_size": os.path.getsize(filepath) if os.path.exists(filepath) else 0,
    }
    
    # Добавляем анализ удобочитаемости
    readability = text_utils.analyze_text_readability(content)
    results.update(readability)
    
    # Добавляем топ-5 самых частотных слов
    most_common = text_utils.get_most_common_words(content, 3)
    results["top_words"] = ", ".join([f"{word}({count})" for word, count in most_common])
    
    print(f"    ✓ Слов: {results['word_count']}, Уникальных: {results['unique_words']}, TTR: {results['ttr']:.3f}")
    
    return results


def analyze_corpus(corpus_folder: str = "corpus") -> List[Dict[str, Any]]:
    """
    Анализирует все текстовые файлы в папке.
    
    Args:
        corpus_folder (str): Путь к папке с текстами
        
    Returns:
        List[Dict[str, Any]]: Список словарей с результатами анализа
    """
    print(f"\n{'='*60}")
    print(f" НАЧИНАЮ АНАЛИЗ КОРПУСА")
    print(f" Папка: {corpus_folder}")
    print(f"{'='*60}")
    
    # Получаем список текстовых файлов
    text_files = file_utils.get_files_in_folder(corpus_folder, ".txt")
    
    if not text_files:
        print(f" В папке '{corpus_folder}' не найдено текстовых файлов (.txt).")
        return []
    
    print(f" Найдено файлов для анализа: {len(text_files)}")
    print("-" * 60)
    
    results = []
    
    # Анализируем каждый файл
    for i, filepath in enumerate(sorted(text_files), 1):
        filename = os.path.basename(filepath)
        print(f"[{i:2d}/{len(text_files):2d}]", end="")
        
        result = analyze_single_text(filepath, filename)
        if result:
            results.append(result)
    
    print(f"\n Анализ завершен. Обработано файлов: {len(results)}")
    
    return results


def load_metadata(metadata_path: str = "data/metadata.csv") -> Dict[str, Dict]:
    """
    Загружает метаданные из CSV файла.
    
    Args:
        metadata_path (str): Путь к файлу метаданных
        
    Returns:
        Dict[str, Dict]: Словарь с метаданными, ключ - имя файла
    """
    metadata = {}
    
    if os.path.exists(metadata_path):
        print(f"\n Загружаю метаданные из {metadata_path}")
        data = file_utils.read_csv_file(metadata_path)
        
        if data:
            for item in data:
                filename = item.get("filename", "")
                if filename:
                    metadata[filename] = item
            print(f"   Загружено записей: {len(metadata)}")
    else:
        print(f"\n Файл метаданных не найден: {metadata_path}")
        print("   Создайте файл data/metadata.csv с информацией о текстах")
    
    return metadata


def enrich_results_with_metadata(results: List[Dict], metadata: Dict[str, Dict]) -> List[Dict]:
    """
    Обогащает результаты анализа метаданными.
    
    Args:
        results (List[Dict]): Результаты анализа
        metadata (Dict[str, Dict]): Метаданные
        
    Returns:
        List[Dict]: Обогащенные результаты
    """
    if not metadata:
        return results
    
    for result in results:
        filename = result.get("filename", "")
        if filename in metadata:
            # Добавляем метаданные к результатам
            result.update(metadata[filename])
    
    return results


def generate_report(results: List[Dict], corpus_name: str = "Текстовый корпус") -> str:
    """
    Создаёт текстовый отчёт на основе результатов анализа.
    
    Args:
        results (List[Dict]): Результаты анализа файлов
        corpus_name (str): Название корпуса
        
    Returns:
        str: Текстовый отчёт
    """
    if not results:
        return "Нет данных для отчета."
    
    report_lines = []
    
    # Заголовок отчета
    report_lines.append("=" * 80)
    report_lines.append(f" ОТЧЁТ ПО АНАЛИЗУ КОРПУСА: {corpus_name}")
    report_lines.append("=" * 80)
    report_lines.append(f"Дата анализа: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Всего текстов: {len(results)}")
    
    # Общая статистика
    report_lines.append("\n" + "=" * 80)
    report_lines.append(" ОБЩАЯ СТАТИСТИКА:")
    report_lines.append("=" * 80)
    
    # Вычисляем общие показатели
    total_words = sum(r.get("word_count", 0) for r in results)
    total_unique_words = sum(r.get("unique_words", 0) for r in results)
    avg_ttr = sum(r.get("ttr", 0) for r in results) / len(results) if results else 0
    avg_word_length = sum(r.get("avg_word_length", 0) for r in results) / len(results) if results else 0
    
    report_lines.append(f"\n Основные показатели:")
    report_lines.append(f"  • Всего слов: {total_words:,}")
    report_lines.append(f"  • Уникальных слов: {total_unique_words:,}")
    report_lines.append(f"  • Средний TTR: {avg_ttr:.4f}")
    report_lines.append(f"  • Средняя длина слова: {avg_word_length:.2f} симв.")
    
    # Находим экстремальные значения
    if results:
        max_words = max(results, key=lambda x: x.get("word_count", 0))
        min_words = min(results, key=lambda x: x.get("word_count", 0))
        max_ttr = max(results, key=lambda x: x.get("ttr", 0))
        min_ttr = min(results, key=lambda x: x.get("ttr", 0))
        
        report_lines.append(f"\n Рекорды:")
        report_lines.append(f"  • Самый объемный текст: {max_words.get('filename')} ({max_words.get('word_count', 0)} слов)")
        report_lines.append(f"  • Самый краткий текст: {min_words.get('filename')} ({min_words.get('word_count', 0)} слов)")
        report_lines.append(f"  • Наибольшее разнообразие (TTR): {max_ttr.get('filename')} ({max_ttr.get('ttr', 0):.4f})")
        report_lines.append(f"  • Наименьшее разнообразие (TTR): {min_ttr.get('filename')} ({min_ttr.get('ttr', 0):.4f})")
    
    # Детальная статистика по каждому файлу
    report_lines.append("\n" + "=" * 80)
    report_lines.append(" ДЕТАЛЬНАЯ СТАТИСТИКА ПО ФАЙЛАМ:")
    report_lines.append("=" * 80)
    
    for i, result in enumerate(results, 1):
        report_lines.append(f"\n{i:3d}.  {result.get('filename', 'Неизвестно')}")
        report_lines.append(f"    {'─' * 70}")
        
        # Основные метаданные если есть
        if "title" in result:
            report_lines.append(f"     Название: {result.get('title', '')}")
        if "author" in result:
            report_lines.append(f"     Автор: {result.get('author', '')}")
        if "year" in result:
            report_lines.append(f"     Год: {result.get('year', '')}")
        
        # Статистика
        report_lines.append(f"     Слов: {result.get('word_count', 0)}")
        report_lines.append(f"     Уникальных слов: {result.get('unique_words', 0)}")
        report_lines.append(f"     TTR: {result.get('ttr', 0):.4f}")
        report_lines.append(f"     Средняя длина слова: {result.get('avg_word_length', 0):.2f} симв.")
        report_lines.append(f"     Строк: {result.get('line_count', 0)}")
        
        if "readability_score" in result:
            score = result.get("readability_score", 0)
            level = "сложный" if score < 50 else "средний" if score < 70 else "простой"
            report_lines.append(f"     Удобочитаемость: {score:.1f}/100 ({level})")
        
        if "top_words" in result and result["top_words"]:
            report_lines.append(f"     Частотные слова: {result.get('top_words', '')}")
    
    # Выводы и интерпретация
    report_lines.append("\n" + "=" * 80)
    report_lines.append(" ВЫВОДЫ И ИНТЕРПРЕТАЦИЯ:")
    report_lines.append("=" * 80)
    
    if results:
        # Анализ разнообразия
        ttr_values = [r.get("ttr", 0) for r in results]
        avg_ttr = sum(ttr_values) / len(ttr_values)
        
        if avg_ttr > 0.7:
            diversity = "высокое лексическое разнообразие"
        elif avg_ttr > 0.5:
            diversity = "среднее лексическое разнообразие"
        else:
            diversity = "низкое лексическое разнообразие"
        
        # Анализ длины слов
        word_lengths = [r.get("avg_word_length", 0) for r in results]
        avg_word_len = sum(word_lengths) / len(word_lengths)
        
        if avg_word_len > 6:
            word_len_desc = "используются длинные слова"
        elif avg_word_len > 4:
            word_len_desc = "средняя длина слов"
        else:
            word_len_desc = "используются короткие слова"
        
        report_lines.append(f"\n Анализ корпуса показывает:")
        report_lines.append(f"  1. Корпус демонстрирует {diversity} (средний TTR: {avg_ttr:.3f})")
        report_lines.append(f"  2. В текстах {word_len_desc} (средняя длина: {avg_word_len:.1f} симв.)")
        report_lines.append(f"  3. Размер текстов варьируется от {min(r.get('word_count', 0) for r in results)} до {max(r.get('word_count', 0) for r in results)} слов")
        
        # Рекомендации
        report_lines.append(f"\n Рекомендации для дальнейшего исследования:")
        report_lines.append(f"  1. Добавить больше текстов для повышения репрезентативности")
        report_lines.append(f"  2. Сравнить с другими корпусами аналогичной тематики")
        report_lines.append(f"  3. Провести анализ по авторам/жанрам если есть метаданные")
    
    report_lines.append("\n" + "=" * 80)
    report_lines.append(f"Отчет сгенерирован: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 80)
    
    return "\n".join(report_lines)


def save_statistics_csv(results: List[Dict], output_path: str = "results/statistics.csv") -> bool:
    """
    Сохраняет результаты анализа в CSV файл.
    
    Args:
        results (List[Dict]): Результаты анализа
        output_path (str): Путь для сохранения CSV файла
        
    Returns:
        bool: True если сохранение успешно, False в противном случае
    """
    if not results:
        print(" Нет результатов для сохранения в CSV")
        return False
    
    # Определяем заголовки для CSV
    # Основные обязательные колонки
    basic_headers = ["filename", "word_count", "unique_words", "ttr"]
    
    # Дополнительные колонки (из результатов)
    additional_headers = []
    if results:
        # Берем все ключи из первого результата, кроме уже добавленных
        sample_keys = list(results[0].keys())
        for key in sample_keys:
            if key not in basic_headers and key not in additional_headers:
                additional_headers.append(key)
    
    # Сортируем дополнительные заголовки для удобства
    additional_headers.sort()
    headers = basic_headers + additional_headers
    
    # Сохраняем в CSV
    success = file_utils.write_csv_file(output_path, results, headers)
    
    if success:
        print(f" Статистика сохранена: {output_path}")
        print(f"   Колонок: {len(headers)}, Записей: {len(results)}")
    
    return success


def main():
    """
    Главная функция программы - точка входа.
    """
    print(" АНАЛИЗ ТЕКСТОВОГО КОРПУСА")
    print("=" * 50)
    print(" Структура проекта:")
    print("  corpus/     - текстовые файлы для анализа")
    print("  data/       - метаданные (metadata.csv)")
    print("  results/    - результаты анализа")
    print("=" * 50)
    
    # Проверяем структуру проекта
    for folder in ["corpus", "data", "results"]:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            print(f"✓ Создана папка: {folder}/")
    
    # Проверяем есть ли файлы для анализа
    text_files = file_utils.get_files_in_folder("corpus", ".txt")
    
    if not text_files:
        print("\n  ВНИМАНИЕ: Папка 'corpus/' пустая!")
        print("   Добавьте текстовые файлы (.txt) в папку 'corpus/'")
        print("   Требуется минимум 20 файлов для анализа")
        return
    
    print(f"\n Найдено текстовых файлов: {len(text_files)}")
    
    if len(text_files) < 5:
        print("  Рекомендуется добавить больше файлов для полноценного анализа")
    
    # Запускаем анализ
    start_time = time.time()
    
    try:
        # 1. Анализируем корпус
        results = analyze_corpus("corpus")
        
        if not results:
            print("\n Не удалось проанализировать файлы")
            return
        
        # 2. Загружаем метаданные
        metadata = load_metadata("data/metadata.csv")
        
        # 3. Обогащаем результаты метаданными
        results = enrich_results_with_metadata(results, metadata)
        
        # 4. Сохраняем статистику в CSV
        print(f"\n Сохраняю результаты...")
        csv_saved = save_statistics_csv(results, "results/statistics.csv")
        
        # 5. Генерируем и сохраняем отчет
        corpus_name = "Мой текстовый корпус"
        if metadata and "author" in next(iter(metadata.values()), {}):
            first_author = next(iter(metadata.values()))["author"]
            corpus_name = f"Корпус произведений {first_author}"
        
        report = generate_report(results, corpus_name)
        report_saved = file_utils.write_text_file("results/report.txt", report)
        
        # 6. Выводим сводку
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*50}")
        print(" АНАЛИЗ ЗАВЕРШЕН УСПЕШНО!")
        print(f"{'='*50}")
        print(f" Обработано текстов: {len(results)}")
        print(f"  Время выполнения: {elapsed_time:.1f} сек.")
        print(f"\n Результаты сохранены в папке 'results/':")
        if csv_saved:
            print(f"  • statistics.csv - таблица с данными")
        if report_saved:
            print(f"  • report.txt - подробный отчет")
        
        # Предлагаем посмотреть отчет
        print(f"\n{'='*50}")
        view = input(" Показать краткий отчет? (да/нет): ").strip().lower()
        
        if view in ['да', 'д', 'yes', 'y', '1']:
            # Показываем только начало отчета
            print("\n" + "=" * 80)
            print(" КРАТКАЯ ВЫБОРКА ИЗ ОТЧЕТА:")
            print("=" * 80)
            lines = report.split('\n')[:30]  # Первые 30 строк
            print('\n'.join(lines))
            print("\n... (полный отчет в results/report.txt)")
        
        print(f"\n Готово!")
            
    except KeyboardInterrupt:
        print("\n\n  Анализ прерван пользователем.")
    except Exception as e:
        print(f"\n Произошла ошибка при анализе: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Устанавливаем кодировку для корректного отображения русских символов
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    main()