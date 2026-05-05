import pytest

from reports import get_report, report_clickbait


def test_report_clickbait_filtering():
    data = [
        {"title": "A", "ctr": 20.0, "retention_rate": 30},
        {"title": "B", "ctr": 10.0, "retention_rate": 50},
        {"title": "C", "ctr": 18.5, "retention_rate": 35},
        {"title": "D", "ctr": 22.0, "retention_rate": 45},  # удержание >40
        {"title": "E", "ctr": 14.0, "retention_rate": 20},  # ctr не >15
    ]
    result = report_clickbait(data)
    titles = [r["title"] for r in result]
    assert titles == ["A", "C"]  # сортировка по убыванию ctr: 20, 18.5


def test_report_clickbait_sorting():
    data = [
        {"title": "X", "ctr": 25.0, "retention_rate": 30},
        {"title": "Y", "ctr": 20.0, "retention_rate": 30},
        {"title": "Z", "ctr": 30.0, "retention_rate": 30},
    ]
    result = report_clickbait(data)
    ctrs = [r["ctr"] for r in result]
    assert ctrs == [30.0, 25.0, 20.0]


def test_report_clickbait_empty():
    data = [
        {"title": "A", "ctr": 10.0, "retention_rate": 80},
        {"title": "B", "ctr": 18.0, "retention_rate": 60},
    ]
    result = report_clickbait(data)
    assert result == []


def test_get_report_known():
    func = get_report("clickbait")
    assert func is report_clickbait


def test_get_report_unknown():
    with pytest.raises(ValueError, match="Неизвестный отчёт 'unknown'"):
        get_report("unknown")
