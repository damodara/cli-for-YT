import pytest

from utils import read_csv_files


def test_read_csv_files_valid(tmp_path):
    content = """title,ctr,retention_rate,extra
Video1,18.2,35,ignored
Video2,22.5,28,ignored
"""
    file1 = tmp_path / "data1.csv"
    file1.write_text(content, encoding="utf-8")

    result = read_csv_files([str(file1)])
    assert len(result) == 2
    assert result[0] == {"title": "Video1", "ctr": 18.2, "retention_rate": 35.0}
    assert result[1] == {"title": "Video2", "ctr": 22.5, "retention_rate": 28.0}


def test_read_csv_files_multiple(tmp_path):
    content1 = "title,ctr,retention_rate\nA,10,20\n"
    content2 = "title,ctr,retention_rate\nB,30,40\n"
    f1 = tmp_path / "f1.csv"
    f2 = tmp_path / "f2.csv"
    f1.write_text(content1)
    f2.write_text(content2)
    result = read_csv_files([str(f1), str(f2)])
    assert len(result) == 2
    assert result[0]["title"] == "A"
    assert result[1]["title"] == "B"


def test_read_csv_files_missing_columns(tmp_path):
    content = "title,views\nVideo,1000\n"
    file = tmp_path / "bad.csv"
    file.write_text(content)
    with pytest.raises(ValueError, match="не содержит обязательные колонки"):
        read_csv_files([str(file)])


def test_read_csv_files_not_found():
    with pytest.raises(FileNotFoundError, match="Файл не найден: missing.csv"):
        read_csv_files(["missing.csv"])


def test_read_csv_files_skip_bad_numbers(tmp_path):
    content = """title,ctr,retention_rate
Good,15.5,30
Bad,not_number,40
"""
    file = tmp_path / "mixed.csv"
    file.write_text(content)
    result = read_csv_files([str(file)])
    assert len(result) == 1
    assert result[0]["title"] == "Good"
