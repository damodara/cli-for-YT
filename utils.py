import csv
from typing import Dict, List


def read_csv_files(file_paths: List[str]) -> List[Dict]:
    """
    Читает один или несколько CSV файлов и возвращает список словарей,
    содержащих только поля title, ctr, retention_rate.
    Поля ctr и retention_rate преобразуются в float.
    Пропускает строки с некорректными числовыми значениями.
    """
    combined = []
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                # Проверяем наличие обязательных колонок
                required = {"title", "ctr", "retention_rate"}
                if not required.issubset(reader.fieldnames):
                    raise ValueError(
                        f"Файл {file_path} не содержит обязательные колонки: {required}"
                    )
                for row in reader:
                    try:
                        # Преобразование числовых полей
                        ctr = float(row["ctr"])
                        retention = float(row["retention_rate"])
                        combined.append(
                            {
                                "title": row["title"],
                                "ctr": ctr,
                                "retention_rate": retention,
                            }
                        )
                    except ValueError:
                        # Пропускаем строки с некорректными числами
                        continue
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {file_path}")
    return combined
