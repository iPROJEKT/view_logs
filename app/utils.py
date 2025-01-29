import re
from datetime import datetime

import numpy as np
from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomPoints, GeomNode, Point3


def extract_prog_number(filename):
    # Ищем номер программы
    match_prog = re.match(r'prog(\d+)_', filename)
    prog_number = int(match_prog.group(1)) if match_prog else 0

    # Ищем дату в формате 'день-месяц-год'
    match_date = re.search(r'(\d{1,2}-\d{1,2}-\d{4})', filename)
    if match_date:
        # Преобразуем строку даты в объект datetime
        date_str = match_date.group(1)
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    else:
        # Если дата не найдена, присваиваем минимальную дату
        date_obj = datetime.min

    print(prog_number, date_obj)  # Для отладки
    return (prog_number, date_obj)


def on_date_selected(start_date, end_date):
    """Обработчик ввода диапазона дат."""
    try:
        # Преобразуем строки в объекты datetime
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        if end_date_obj >= start_date_obj:
            return 0
        else:
            return 1
    except ValueError:
        return 1


def load_log_data(file_path):
    """Загружает данные из файла и возвращает координаты и параметры."""
    data = []
    i_values, u_values, wfs_values = [], [], []

    with open(file_path, 'r') as file:
        for line in file:
            # Пропускаем пустые строки или строки, которые не содержат ожидаемые данные
            if line.strip() == '':
                continue

            values = line.split(';')
            if len(values) >= 18:  # Убедимся, что индексы существуют
                try:
                    # Читаем координаты и параметры
                    x = float(values[9].strip())
                    y = float(values[10].strip())
                    z = float(values[11].strip())
                    i = float(values[15].strip())
                    u = float(values[16].strip())
                    wfs = float(values[17].strip())

                    # Сохраняем данные
                    data.append((x, y, z))
                    i_values.append(i)
                    u_values.append(u)
                    wfs_values.append(wfs)
                except ValueError:
                    # Игнорируем строки с некорректными значениями
                    continue

    if not data:
        print("Нет данных для отображения.")
        return None, None, None, None

    return data, i_values, u_values, wfs_values


def normalize_parameter(param_values, custom_min=None, custom_max=None):
    """Нормализует значения параметра в диапазон [0, 1], с клипингом."""
    param_min = custom_min if custom_min is not None else min(param_values)
    param_max = custom_max if custom_max is not None else max(param_values)

    if param_min == param_max:
        print("Минимум и максимум совпадают. Нормализация невозможна.")
        return [0.5] * len(param_values)

    normalized = [(val - param_min) / (param_max - param_min) for val in param_values]

    print(f"Параметр до нормализации: {param_values[:5]}")
    print(f"Диапазон нормализации: [{param_min}, {param_max}]")
    print(f"Нормализованные значения: {normalized[:5]}")

    return [max(0, min(1, norm)) for norm in normalized]


def generate_roygb_gradient(length_grad):
    """Создает градиент цветов от зелёного до красного."""
    royg_gradient = np.zeros((length_grad + 1, 3))

    # Функции для вычисления цветовых значений для каждого перехода
    def green_to_yellow(i, section):
        return [i / section, 1, 0]

    def yellow_to_red(i, section):
        return [1, 1 - (i - section) / section, 0]

    section = length_grad // 2  # Делим на две части: зелёный->жёлтый, жёлтый->красный

    # Заполнение градиента
    for i in range(length_grad + 1):
        if i <= section:
            royg_gradient[i] = green_to_yellow(i, section)
        else:
            royg_gradient[i] = yellow_to_red(i, section)

    return royg_gradient


def create_point_cloud(data, param_normalized, royg_gradient, length_grad, parent):
    """Создает облако точек с градиентом."""
    vertex_data = GeomVertexData("log_point_cloud", GeomVertexFormat.get_v3c4(), Geom.UH_static)
    vertex_writer = GeomVertexWriter(vertex_data, "vertex")
    color_writer = GeomVertexWriter(vertex_data, "color")

    for (x, y, z), param_norm in zip(data, param_normalized):
        vertex_writer.addData3f(x, y, z)

        # Нормализуем grad_index, чтобы он не выходил за границы
        grad_index = int(max(0, min(param_norm * (length_grad - 1), length_grad - 1)))  # Границы 0 и length_grad-1

        color = royg_gradient[grad_index]
        color_writer.addData4f(color[0], color[1], color[2], 1.0)

    points = Geom(vertex_data)
    primitive = GeomPoints(Geom.UH_static)
    primitive.addNextVertices(len(data))
    points.addPrimitive(primitive)

    geom_node = GeomNode("log_point_cloud_node")
    geom_node.addGeom(points)
    node_path = parent.attachNewNode(geom_node)

    return node_path


def load_logs_and_create_point_cloud(
        file_path, parent, gradient_param='I', length_grad=256, custom_min=None, custom_max=None,
        filter_type="All"
):
    """Основная функция, которая загружает логи, нормализует данные, создает градиент и облако точек."""

    # 1. Загрузка данных
    data, i_values, u_values, wfs_values = load_log_data(file_path)
    if not data:
        return None, None, None

    # 2. Определение параметра для градиента
    param_values = get_gradient_param_values(gradient_param, i_values, u_values, wfs_values)
    if param_values is None:
        return None, None, None

    # 3. Фильтрация данных
    filtered_data = filter_data(data, param_values, filter_type, custom_min, custom_max)
    if not filtered_data:
        print(f"Файл {file_path}: нет точек для отображения после фильтрации.")
        return None, None, None

    # 4. Разделяем обратно координаты и параметры
    data, param_values = zip(*filtered_data)

    # 5. Вычисление диапазона Z
    z_min, z_max = compute_z_range(data)

    # 6. Нормализация параметров
    param_normalized = normalize_parameter(param_values, custom_min, custom_max)
    if param_normalized is None:
        return None, None, None

    # 7. Генерация градиента
    royg_gradient = generate_roygb_gradient(length_grad)

    # 8. Создание облака точек
    node_path = create_point_cloud(data, param_normalized, royg_gradient, length_grad, parent)

    return node_path, [point[2] for point in data], (z_min, z_max)


def get_gradient_param_values(gradient_param, i_values, u_values, wfs_values):
    """Возвращает значения параметров для градиента в зависимости от выбора."""
    if gradient_param == 'I':
        return i_values
    elif gradient_param == 'U':
        return u_values
    elif gradient_param == 'WFS':
        return wfs_values
    else:
        print("Неверный параметр для градиента.")
        return None


def filter_data(data, param_values, filter_type, custom_min, custom_max):
    """Фильтрует данные в зависимости от типа фильтра и заданных границ."""
    if filter_type == "Into" and custom_min is not None and custom_max is not None:
        return [(point, param) for point, param in zip(data, param_values)
                if custom_min <= param <= custom_max]
    elif filter_type == "Out" and custom_min is not None and custom_max is not None:
        return [(point, param) for point, param in zip(data, param_values)
                if param < custom_min or param > custom_max]
    else:  # Для "All" просто используем все данные
        return list(zip(data, param_values))


def compute_z_range(data):
    """Вычисляет минимальное и максимальное значение по оси Z."""
    z_values = [point[2] for point in data]
    return min(z_values), max(z_values)


def calculate_center(points):
    """Вычисляет центр по всем точкам."""
    if not points:
        return Point3(0, 0, 0)

    # Суммируем все координаты и делим на количество точек
    x_total, y_total, z_total = 0, 0, 0
    for point in points:
        x_total += point[0]
        y_total += point[1]
        z_total += point[2]

    num_points = len(points)
    return Point3(x_total / num_points, y_total / num_points, z_total / num_points)
