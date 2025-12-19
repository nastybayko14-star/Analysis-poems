import os
import csv
from typing import List, Dict, Optional


def read_text_file(filepath: str) -> Optional[str]:
    """
    Чтение текстового файла с обработкой ошибок.
    
    Args:
        filepath (str): Путь к файлу
        
    Returns:
        Optional[str]: Содержимое файла или None в случае ошибки
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(filepath):
            print(f"Файл {filepath} не найден.")
            return None
        
        # Проверяем, что это файл, а не папка
        if not os.path.isfile(filepath):
            print(f"{filepath} не является файлом.")
            return None
        
        # Читаем файл
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return content
        
    except PermissionError:
        print(f"Нет прав для чтения файла {filepath}")
        return None
    except UnicodeDecodeError:
        print(f"Ошибка декодирования файла {filepath}. Убедитесь, что файл в кодировке UTF-8.")
        return None
    except Exception as e:
        print(f"Неизвестная ошибка при чтении файла {filepath}: {e}")
        return None


def read_csv_file(filepath: str) -> Optional[List[Dict]]:
    """
    Чтение CSV-файла, возврат списка словарей.
    
    Args:
        filepath (str): Путь к CSV-файлу
        
    Returns:
        Optional[List[Dict]]: Список словарей с данными или None в случае ошибки
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(filepath):
            print(f"Файл {filepath} не найден.")
            return None
        
        if not os.path.isfile(filepath):
            print(f"{filepath} не является файлом.")
            return None
        
        data = []
        
        with open(filepath, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            # Проверяем, есть ли заголовки
            if csv_reader.fieldnames is None:
                print(f"CSV файл {filepath} не содержит заголовков.")
                return None
            
            for row in csv_reader:
                data.append(dict(row))
        
        return data
        
    except PermissionError:
        print(f"Нет прав для чтения файла {filepath}")
        return None
    except Exception as e:
        print(f"Ошибка при чтении CSV файла {filepath}: {e}")
        return None


def write_csv_file(filepath: str, data: List[Dict], headers: List[str]) -> bool:
    """
    Запись данных в CSV файл.
    
    Args:
        filepath (str): Путь для сохранения файла
        data (List[Dict]): Данные для записи
        headers (List[str]): Заголовки столбцов
        
    Returns:
        bool: True если запись успешна, False в противном случае
    """
    try:
        # Создаем папку, если она не существует
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=headers)
            
            # Записываем заголовки
            csv_writer.writeheader()
            
            # Записываем данные
            for row in data:
                csv_writer.writerow(row)
        
        print(f"✓ CSV файл успешно сохранен: {filepath}")
        return True
        
    except Exception as e:
        print(f"Ошибка при записи CSV файла {filepath}: {e}")
        return False


def write_text_file(filepath: str, content: str) -> bool:
    """
    Запись текста в файл.
    
    Args:
        filepath (str): Путь для сохранения файла
        content (str): Текст для записи
        
    Returns:
        bool: True если запись успешна, False в противном случае
    """
    try:
        # Создаем папку, если она не существует
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✓ Текстовый файл успешно сохранен: {filepath}")
        return True
        
    except Exception as e:
        print(f"Ошибка при записи текстового файла {filepath}: {e}")
        return False


def get_files_in_folder(folder_path: str, extension: str = None) -> Optional[List[str]]:
    """
    Получение списка файлов в папке с указанным расширением.
    
    Args:
        folder_path (str): Путь к папке
        extension (str, optional): Расширение файлов (например, '.txt')
        
    Returns:
        Optional[List[str]]: Список путей к файлам или None в случае ошибки
    """
    try:
        # Проверяем существование папки
        if not os.path.exists(folder_path):
            print(f"Папка {folder_path} не найдена.")
            return None
        
        if not os.path.isdir(folder_path):
            print(f"{folder_path} не является папкой.")
            return None
        
        files = []
        
        # Обходим файлы в папке (без рекурсии по подпапкам)
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            # Если указано расширение, фильтруем по нему
            if extension:
                if os.path.isfile(item_path) and item.endswith(extension):
                    files.append(item_path)
            else:
                if os.path.isfile(item_path):
                    files.append(item_path)
        
        # Сортируем файлы по алфавиту
        files.sort()
        
        return files
        
    except PermissionError:
        print(f"Нет прав для доступа к папке {folder_path}")
        return None
    except Exception as e:
        print(f"Ошибка при получении списка файлов: {e}")
        return None