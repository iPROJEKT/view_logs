import re
from datetime import datetime


REGULAR_FOR_MATCH = r'(?i)log_(\d+)\.dt'
SELECT_PROG_DATE = '%Y-%m-%d'
EXTRACT_PROG_DATE = '%d-%m-%Y'


def decode_karel_time(encoded_time):
    """
    Декодирует 32-битное время из формата KAREL.
    :param encoded_time: Целое число (32-битное время KAREL).
    :return: Дата и время (datetime) или None при ошибке.
    """
    try:
        fields = {
            "year": ((encoded_time >> 25) & 0b1111111) + 1980,
            "month": (encoded_time >> 21) & 0b1111,
            "day": (encoded_time >> 16) & 0b11111,
            "hour": (encoded_time >> 11) & 0b11111,
            "minute": (encoded_time >> 5) & 0b111111,
            "second": (encoded_time & 0b11111) * 2,
        }
        return datetime(**fields)
    except ValueError:
        return None


def extract_prog_number(filename):
    """
    Извлекает номер программы и дату из имени файла.
    :param filename: Имя файла.
    :return: (номер программы, объект datetime).
    """
    match = re.match(REGULAR_FOR_MATCH, filename)
    if match:
        try:
            encoded_time = int(match.group(1))
            decoded_date = decode_karel_time(encoded_time)
            return 0, decoded_date if decoded_date else datetime.min
        except ValueError:
            pass
    return 0, datetime.min


def on_date_selected(start_date, end_date):
    """
    Проверяет валидность диапазона дат.
    :param start_date: Начальная дата (строка 'YYYY-MM-DD').
    :param end_date: Конечная дата (строка 'YYYY-MM-DD').
    :return: 0, если диапазон валиден, 1 при ошибке.
    """
    try:
        start_date_obj = datetime.strptime(start_date, SELECT_PROG_DATE)
        end_date_obj = datetime.strptime(end_date, SELECT_PROG_DATE)
        return 0 if end_date_obj >= start_date_obj else 1
    except ValueError:
        return 1


def filter_by_date(filename, start_date, end_date):
    """
    Фильтрует файлы по диапазону дат.
    :param filename: Имя файла.
    :param start_date: Начальная дата (строка в формате 'YYYY-MM-DD').
    :param end_date: Конечная дата (строка в формате 'YYYY-MM-DD').
    :return: True, если файл попадает в диапазон, иначе False.
    """
    _, file_date = extract_prog_number(filename)
    if start_date and end_date:
        start_date_obj = datetime.strptime(start_date, SELECT_PROG_DATE)
        end_date_obj = datetime.strptime(end_date, SELECT_PROG_DATE)
        return start_date_obj <= file_date <= end_date_obj
    return True
