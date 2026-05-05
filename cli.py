import argparse
import sys

from tabulate import tabulate

from reports import get_report
from utils import read_csv_files


def main():
    parser = argparse.ArgumentParser(description="Анализ метрик YouTube видео")
    parser.add_argument(
        "--files", nargs="+", required=True, help="Пути к CSV файлам с данными"
    )
    parser.add_argument(
        "--report", required=True, help="Название отчёта (например: clickbait)"
    )
    args = parser.parse_args()

    # Чтение данных из всех указанных файлов
    try:
        data = read_csv_files(args.files)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неизвестная ошибка при чтении файлов: {e}", file=sys.stderr)
        sys.exit(1)

    # Получение функции-отчёта
    try:
        report_func = get_report(args.report)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    # Формирование отчёта
    try:
        report_data = report_func(data)
    except Exception as e:
        print(f"Ошибка при формировании отчёта: {e}", file=sys.stderr)
        sys.exit(1)

    # Вывод таблицы
    if report_data:
        print(tabulate(report_data, headers="keys", tablefmt="grid"))
    else:
        print("Нет данных, соответствующих условиям отчёта.")


if __name__ == "__main__":
    main()
