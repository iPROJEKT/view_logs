from datetime import datetime


SELECT_PROG_DATE = '%Y-%m-%d'
EXTRACT_PROG_DATE = '%d-%m-%Y'


def on_date_selected(start_date, end_date):
    """
    Обработчик ввода диапазона дат.
    :param start_date: Начальная дата (строка в формате 'YYYY-MM-DD').
    :param end_date: Конечная дата (строка в формате 'YYYY-MM-DD').
    :return: 0, если диапазон валиден, иначе 1.
    """
    try:
        start_date_obj = datetime.strptime(start_date, SELECT_PROG_DATE)
        end_date_obj = datetime.strptime(end_date, SELECT_PROG_DATE)
        if end_date_obj >= start_date_obj:
            return 0
        else:
            return 1
    except ValueError:
        return 1
