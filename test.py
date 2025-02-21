def decode_karel_time(encoded_time):
    """
    Декодирует 32-битное время из формата KAREL.

    :param encoded_time: Целое число (32-битное время KAREL).
    :return: Расшифрованная дата и время в формате "YYYY-MM-DD HH:MM:SS".
    """
    # Извлекаем поля из битов
    year = ((encoded_time >> 25) & 0b1111111) + 1980  # Биты 31–25, год с 1980 года
    month = (encoded_time >> 21) & 0b1111  # Биты 24–21, месяц (1–12)
    day = (encoded_time >> 16) & 0b11111  # Биты 20–16, день месяца (1–31)
    hour = (encoded_time >> 11) & 0b11111  # Биты 15–11, часы (0–23)
    minute = (encoded_time >> 5) & 0b111111  # Биты 10–5, минуты (0–59)
    two_second_increments = encoded_time & 0b11111  # Биты 4–0, 2-секундные инкременты (0–29)
    second = two_second_increments * 2  # Переводим в секунды

    # Формируем дату и время
    return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"


# Пример использования
encoded_time = 1515414610
decoded_time = decode_karel_time(encoded_time)
print("Расшифрованное время:", decoded_time)
