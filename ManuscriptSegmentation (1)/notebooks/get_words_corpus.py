import unicodedata
import pandas as pd
import numpy as np

import os
import re
import unicodedata

def get_raw_lines_from_doc(file_path):
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден!")
        return []

    with os.popen(f'antiword "{file_path}"') as pipe:
        text = pipe.read()

    return text.splitlines()

import re

def get_clean_words(raw_lines):
    # Паттерн: оставляем только нужные буквы, титла и разделитель-точку
    pattern = re.compile(r'[^а-яА-ЯёЁ\u0400-\u04FF\uA640-\uA69F\u0300-\u036F·\-\s]')

    full_text = []

    for line in raw_lines:
        line = re.sub(r'\d+[a-гв]?\s*', '', line).strip()
        # 1. Удаляем всё, что не входит в наш славянский паттерн (цифры пагинации и т.д.)
        line = pattern.sub('', line)
        # 2. Нормализуем пробелы
        line = ' '.join(line.split())
        if line:
            full_text.append(line)

    # Склеиваем всё в одну строку для обработки переносов
    combined_text = " ".join(full_text[1:])

    # 3. Обработка переносов: "же- нѹ" -> "женѹ"
    # Ищем дефис, за которым следуют пробелы и после часть слова
    combined_text = re.sub(r'-\s+', '', combined_text)
    print(combined_text[:100])

    # Очищаем от точек-разделителей, чтобы они не липли к словам в словаре
    words = [w.strip('·') for w in combined_text.split() if len(w.strip('·')) > 0]

    return words