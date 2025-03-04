import os
import numpy as np
from datetime import datetime
from panda3d.core import (
    GeomVertexData, GeomVertexWriter, GeomVertexReader,
    GeomVertexFormat, Geom, GeomPoints,
    GeomNode, Point3, LineSegs, LPoint3f
)
from app.core.tools.const import LOGS_DIR


def load_log_data(file_path):
    """Загружает данные из файла и возвращает координаты и параметры."""
    data = []
    i_values, u_values, wfs_values = [], [], []
    gi7_values, gi8_values, gi10_values, gi11_values = [], [], [], []

    try:
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                values = line.strip().split(';')
                if len(values) < 18:
                    continue
                try:
                    x, y, z = map(float, values[9:12])
                    i, u, wfs = map(float, values[15:18])
                    gi7, gi8, gi9, gi10 = map(float, values[-4:])
                    data.append((x, y, z))
                    i_values.append(i)
                    u_values.append(u)
                    wfs_values.append(wfs)
                    gi7_values.append(gi7)
                    gi8_values.append(gi8)
                    gi10_values.append(gi9)
                    gi11_values.append(gi10)
                except ValueError as e:
                    continue
    except (OSError, IOError) as e:
        print(f"Ошибка чтения файла {file_path}: {e}")

    return data, i_values, u_values, wfs_values, gi7_values, gi8_values, gi10_values, gi11_values


def normalize_parameter(param_values, custom_min=None, custom_max=None):
    """Нормализует значения параметра в диапазон [0, 1], с клипингом."""
    if custom_min is not None and custom_max is not None:
        param_min = float(custom_min)
        param_max = float(custom_max)
    else:
        param_min = min(param_values)
        param_max = max(param_values)

    if param_min == param_max:
        print("Минимум и максимум совпадают. Нормализация невозможна.")
        return [0.5] * len(param_values)
    normalized = [(val - param_min) / (param_max - param_min) for val in param_values]
    return [max(0, min(1, norm)) for norm in normalized]


def generate_roygb_gradient(length_grad):
    """Создает градиент цветов от зелёного до красного в RGB."""
    royg_gradient = np.zeros((length_grad + 1, 3))
    section = length_grad // 2
    for i in range(length_grad + 1):
        if i <= section:
            royg_gradient[i] = [i / section, 1, 0]  # green_to_yellow
        else:
            royg_gradient[i] = [1, 1 - (i - section) / section, 0]  # yellow_to_red
    return royg_gradient


def create_point_cloud(data, param_normalized, royg_gradient, length_grad, parent, point_size=1.0):
    """Создает облако точек с градиентом в RGB, записывая в BGR."""
    vertex_data = GeomVertexData("log_point_cloud", GeomVertexFormat.get_v3c4(), Geom.UH_static)
    vertex_writer = GeomVertexWriter(vertex_data, "vertex")
    color_writer = GeomVertexWriter(vertex_data, "color")

    for i, ((x, y, z), param_norm) in enumerate(zip(data, param_normalized)):
        vertex_writer.addData3f(x, y, z)
        grad_index = int(max(0, min(param_norm * (length_grad - 1), length_grad - 1)))
        color = royg_gradient[grad_index]
        color_writer.addData4f(color[0], color[1], color[2], 1.0)

    points = Geom(vertex_data)
    primitive = GeomPoints(Geom.UH_static)
    primitive.addNextVertices(len(data))
    points.addPrimitive(primitive)

    geom_node = GeomNode("log_point_cloud_node")
    geom_node.addGeom(points)

    node_path = parent.attachNewNode(geom_node)
    node_path.setRenderModeThickness(int(point_size))
    node_path.setLightOff(1)
    node_path.setColorOff(1)
    node_path.setShaderAuto()
    return node_path


def create_lines_cloud(data, param_normalized, royg_gradient, length_grad, parent, line_thickness=1.0):
    """Создает облако линий с градиентом."""
    if len(data) < 2:
        print("Ошибка: недостаточно точек для построения линий.")
        return None

    line_segs = LineSegs()
    line_segs.setThickness(float(line_thickness))

    for i in range(len(data) - 1):
        # Начало и конец линии
        start_point = data[i]
        end_point = data[i + 1]

        # Градиентный цвет для начальной и конечной точки
        start_norm = param_normalized[i]
        end_norm = param_normalized[i + 1]

        start_index = int(max(0, min(start_norm * (length_grad - 1), length_grad - 1)))
        end_index = int(max(0, min(end_norm * (length_grad - 1), length_grad - 1)))

        start_color = royg_gradient[start_index]
        end_color = royg_gradient[end_index]

        line_segs.setColor(start_color[0], start_color[1], start_color[2], 1.0)
        line_segs.moveTo(*start_point)
        line_segs.setColor(end_color[0], end_color[1], end_color[2], 1.0)
        line_segs.drawTo(*end_point)

    node = line_segs.create()
    node_path = parent.attachNewNode(node)
    return node_path


def load_logs_and_create_point_cloud(
    file_path, parent,
    gradient_param='I',
    length_grad=256,
    custom_min=None,
    custom_max=None,
    filter_type="All",
    point_size=1.0,
    point_step=1,
    point=True
):
    """Основная функция, которая загружает логи, нормализует данные, создает градиент и облако точек."""
    try:
        int(point_step)
        int(point_size)
    except Exception:
        return
    if int(point_step) <= 0:  # Проверяем шаг
        print("Ошибка: значение point_step должно быть больше 0. Установлено значение по умолчанию: 1.")
        point_step = 1
    if int(point_size) <= 0:
        point_size = 1

    data, i_values, u_values, wfs_values, GI7_values, GI8_values, GI9_values, GI10_values = load_log_data(file_path)
    if not data:
        return None, None, None, None, None, None, None
    data = data[::int(point_step)]
    i_values = i_values[::int(point_step)]
    u_values = u_values[::int(point_step)]
    wfs_values = wfs_values[::int(point_step)]
    GI7_values = GI7_values[::int(point_step)]
    GI8_values = GI8_values[::int(point_step)]
    GI9_values = GI9_values[::int(point_step)]
    GI10_values = GI10_values[::int(point_step)]

    param_values = get_gradient_param_values(
        gradient_param, i_values, u_values, wfs_values,
        GI7_values, GI8_values, GI9_values, GI10_values
    )
    if param_values is None:
        return None, None, None

    filtered_data = filter_data(data, param_values, filter_type, custom_min, custom_max)
    if not filtered_data:
        return None, None, None

    data, param_values = zip(*filtered_data)
    z_min, z_max = compute_z_range(data)
    param_normalized = normalize_parameter(param_values, custom_min, custom_max)
    if param_normalized is None:
        return None, None, None

    royg_gradient = generate_roygb_gradient(length_grad)
    if point:
        node_path = create_point_cloud(
            data, param_normalized, royg_gradient,
            length_grad, parent, point_size
        )
    else:
        node_path = create_lines_cloud(
            data, param_normalized, royg_gradient,
            length_grad, parent, point_size
        )
    return node_path, [point[2] for point in data], (z_min, z_max), data


def get_gradient_param_values(
    gradient_param, i_values, u_values, wfs_values,
        GI7_values, GI8_values, GI9_values, GI10_values
):
    """Возвращает значения параметров для градиента в зависимости от выбора."""
    if gradient_param == 'I':
        return i_values
    elif gradient_param == 'U':
        return u_values
    elif gradient_param == 'WFS':
        return wfs_values
    elif gradient_param == 'pres1':
        return GI7_values
    elif gradient_param == 'pres2':
        return GI8_values
    elif gradient_param == 'flow1':
        return GI9_values
    elif gradient_param == 'flow2':
        return GI10_values
    else:
        return i_values


def filter_data(data, param_values, filter_type, custom_min, custom_max):
    """Фильтрует данные в зависимости от типа фильтра и заданных границ."""
    if filter_type == "Into" and custom_min is not None and custom_max is not None:
        return [(point, param) for point, param in zip(data, param_values)
                if custom_min <= param <= custom_max]
    elif filter_type == "Out" and custom_min is not None and custom_max is not None:
        return [(point, param) for point, param in zip(data, param_values)
                if param < custom_min or param > custom_max]
    else:
        return list(zip(data, param_values))


def compute_z_range(data):
    z_values = [point[2] for point in data]
    return min(z_values), max(z_values)


def calculate_center(points):
    if not points:
        print("Ошибка: список точек пуст. Центр установлен в (0, 0, 0).")
        return LPoint3f(0, 0, 0)
    num_points = len(points)
    x, y, z = map(sum, zip(*points))
    return LPoint3f(x / num_points, y / num_points, z / num_points)


def get_result(file_path, parent, gradient_param, custom_min, custom_max, filter_type, size, point_step, point):
    node_path = None
    result = load_logs_and_create_point_cloud(
        file_path=file_path,
        parent=parent,
        gradient_param=gradient_param,
        custom_min=custom_min,
        custom_max=custom_max,
        filter_type=filter_type,
        point_size=size,
        point_step=point_step,
        point=point
    )
    if result:
        if isinstance(result, tuple):
            node_path = result[0]
        else:
            node_path = result

    return node_path
