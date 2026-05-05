from typing import Callable, Dict, List


def report_clickbait(data: List[Dict]) -> List[Dict]:
    """
    Отчёт "clickbait": видео с CTR > 15 и удержанием < 40.
    Сортировка по убыванию CTR.
    """
    filtered = [
        row
        for row in data
        if row.get("ctr", 0) > 15 and row.get("retention_rate", 100) < 40
    ]
    sorted_data = sorted(filtered, key=lambda x: x["ctr"], reverse=True)
    # Возвращаем только нужные колонки
    return [
        {
            "title": row["title"],
            "ctr": row["ctr"],
            "retention_rate": row["retention_rate"],
        }
        for row in sorted_data
    ]


# Регистр доступных отчётов (название -> функция)
_REPORTS: Dict[str, Callable] = {
    "clickbait": report_clickbait,
}


def get_report(name: str) -> Callable:
    """
    Возвращает функцию-отчёт по её имени.
    Если отчёт не найден, выбрасывает ValueError.
    """
    if name not in _REPORTS:
        available = ", ".join(_REPORTS.keys())
        raise ValueError(f"Неизвестный отчёт '{name}'. Доступные отчёты: {available}")
    return _REPORTS[name]
