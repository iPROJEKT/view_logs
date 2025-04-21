import os
import threading
from datetime import datetime, timedelta

from panda3d.core import NodePath

from app.core.tools.const import LOGS_DIR
from app_ref.Sceen3.utils import extract_prog_number
from app_ref.Scene4.ButtonUI import ButtonsUI
from app_ref.Scene4.FrameUI import FramesUI
from app_ref.Scene4.HelpTextUI import HelpTextUI
from app_ref.Scene4.ImageUI import ImageUI
from app_ref.Scene4.InputUI import InputUI
from app_ref.Scene4.PopUi import PopMenuUI
from app_ref.Scene4.SliderUI import SliderUI
from app_ref.Scene4.error import ErrorDialogsUI
from app_ref.Scene4.utils import load_logs_and_create_point_cloud, calculate_center, get_result
from app_ref.SceneABS.SceneABS import Screen
from app_ref.camera_control.camera import CameraControl
from app_ref.config import ConfigApp


class Scene4(Screen):
    def __init__(self, name, base, switch_callback):
        super().__init__(name, base)
        self.name = name
        self.config_app = ConfigApp()
        self.center_node = (0, 0, 0)
        self.camera_control = None
        self.file_names = []
        self.empty_file = []
        self.poit_mode = True
        self.point_cloud_nodes = []
        self.selected_file = None
        self.slider_timer = None
        self.point_size = 1.0
        self.point_step = 1
        self.all_data_point = []
        self.right_time_slider = 0
        self.left_time_slider = 0
        self.switch_callback = switch_callback

        self.ui_node = self.node.attachNewNode("UI_Scene4")

        self.frames = FramesUI(self.config_app)
        self.image = ImageUI(self.config_app)
        self.slider = SliderUI()
        self.slider.slider.scene_ref = self
        self.help_text = HelpTextUI(
            self.config_app,
            self.frames.left_user_frame,
            base,
            ri='',
            le=''
        )
        self.pop_menu = PopMenuUI(
            self.config_app,
            self.frames.filter_frame,
            self.frames.value_frame,
            base,
            top=self.help_text.help_text_top,
            bottom=self.help_text.help_text_bottom
        )
        self.buttons = ButtonsUI(
            self.ui_node,
            base,
            self.config_app,
            self.frames.left_user_frame,
            text=self.help_text.choice_text,
            point_mode=self.poit_mode,
            scene=self,
            slider=self.slider.slider,
            ri=self.help_text.slider_right_time,
            le=self.help_text.slider_left_time,
            update=lambda: self.update_layers(),
            on_back_button_from_point=self.on_back_button_from_point
        )
        self.input = InputUI(
            self.config_app,
            self.frames.left_user_frame,
            base
        )
        self.error = ErrorDialogsUI(
            self.config_app,
            base,
            node=self.node,
            button=self.buttons.open_left_panel_button,
        )

        self.slider.slider['command'] = self.on_slider_change

    def on_param_change(self, *args):
        """Обработчик изменения параметров UI."""
        print(f"[DEBUG] Параметры изменены: gradient_param={self.pop_menu.magnitude_menu.get()}, "
              f"filter_type={self.pop_menu.magnitude_menu_filter.get()}, "
              f"custom_min={self.input.number_input_bottom.get()}, "
              f"custom_max={self.input.number_input_top.get()}, "
              f"point_size={self.input.size_input.get()}, "
              f"point_step={self.input.spliter_input.get()}")
        self.update_layers()

    def clear_point_cloud_nodes(self):
        """Очищает все текущие облака точек."""
        print(f"[DEBUG] Очистка {len(self.point_cloud_nodes)} облаков точек")
        for node in self.point_cloud_nodes:
            if isinstance(node, tuple):
                node_path = node[0]
            else:
                node_path = node
            if isinstance(node_path, NodePath):
                print(f"[DEBUG] Удаление node_path={node_path}")
                node_path.removeNode()
        self.point_cloud_nodes.clear()

    def on_back_button_from_point(self):
        """Скрывает все элементы сцены, очищает данные и переключает на Scene3."""
        try:
            print("[DEBUG] Back button pressed")
            self.hide_fields()
            self.node.hide()
            self.clear_point_cloud_nodes()
            if self.camera_control:
                try:
                    self.camera_control.cleanup()
                except AttributeError:
                    print("[DEBUG] CameraControl has no cleanup method, skipping")
                self.camera_control = None
            self.file_names = []
            self.all_data_point = []
            self.left_time_slider = 0
            self.right_time_slider = 0
            self.update_slider_text()
            self.switch_callback(3)
        except Exception as e:
            print(f"[ERROR] Exception in on_back_button_from_point: {e}")

    def hide_fields(self):
        """Скрывает все поля UI."""
        print("[DEBUG] Hiding fields")
        self.buttons.open_left_panel_button.hide()
        self.buttons.back_button_from_point.hide()
        self.help_text.help_text_top.hide()
        self.help_text.help_text_bottom.hide()
        self.help_text.alt_cam.hide()
        self.input.number_input_top.hide()
        self.input.number_input_bottom.hide()
        self.image.image_label.hide()
        self.slider.slider.hide()
        self.help_text.slider_left_time.hide()
        self.help_text.slider_right_time.hide()
        if self.camera_control:
            try:
                self.camera_control.axes_node.hide()
                self.camera_control.compass_node.hide()
            except AttributeError:
                print("[DEBUG] CameraControl has no axes_node or compass_node, skipping")

    def on_slider_change(self):
        """Обработчик изменения слайдера для управления слоями."""
        slider_value = self.slider.slider['value']
        print(f"[DEBUG] Слайдер изменен: slider_value={slider_value}")
        if self.slider_timer is not None:
            self.slider_timer.cancel()
        self.slider_timer = threading.Timer(0.5, self.update_layers, args=(slider_value,))
        self.slider_timer.start()

    def update_layers(self, slider_value=None):
        """Обновляет отображаемые слои пропорционально положению слайдера."""
        if slider_value is None:
            slider_value = self.slider.slider['value']

        if not self.file_names:
            print("[DEBUG] Нет файлов для отображения")
            return

        try:
            left_dt = datetime.strptime(self.left_time_slider, '%Y-%m-%d %H:%M')
            right_dt = datetime.strptime(self.right_time_slider, '%Y-%m-%d %H:%M')
            time_range = (right_dt - left_dt).total_seconds()
            if time_range <= 0:
                print("[DEBUG] Некорректный временной диапазон")
                self.error.show_error("Ошибка: конечное время должно быть позже начального. Пожалуйста, выберите корректный диапазон.")
                return
        except ValueError as e:
            print(f"[DEBUG] Ошибка парсинга времени: {e}")
            self.error.show_error(f"Ошибка формата времени: {e}")
            return

        visible_layers = int((slider_value / 100) * len(self.file_names))
        print(f"[DEBUG] Обновление слоев: visible_layers={visible_layers}, total_files={len(self.file_names)}")
        self.clear_point_cloud_nodes()
        self.update_point_cloud_nodes(visible_layers)

    def update_point_cloud_nodes(self, visible_layers):
        """Обновляет облака точек, показывая только заданное количество слоев."""
        print(f"[DEBUG] Обновление облаков точек: visible_layers={visible_layers}, file_names={self.file_names[:visible_layers]}")
        empty_files = []
        error_messages = []

        # Валидация параметров
        custom_min = self.input.number_input_bottom.get()
        custom_max = self.input.number_input_top.get()
        try:
            custom_min = float(custom_min) if custom_min else None
            custom_max = float(custom_max) if custom_max else None
            if custom_min is not None and custom_max is not None and custom_min >= custom_max:
                print("[DEBUG] Ошибка: custom_min >= custom_max")
                self.error.show_error("Ошибка: custom_min должен быть меньше custom_max")
                return
        except ValueError:
            print("[DEBUG] Ошибка преобразования custom_min/max")
            self.error.show_error("Ошибка: введены некорректные значения min/max")
            custom_min = None
            custom_max = None

        try:
            size_value = float(self.input.size_input.get()) if self.input.size_input.get() else 1.0
            if size_value <= 0:
                print("[DEBUG] Ошибка: size_value <= 0")
                self.error.show_error("Ошибка: размер точки должен быть больше 0")
                return
        except ValueError:
            print("[DEBUG] Ошибка преобразования size_value")
            self.error.show_error("Ошибка: некорректное значение размера точки")
            return

        try:
            spliter_value = float(self.input.spliter_input.get()) if self.input.spliter_input.get() else 1
            if spliter_value <= 0:
                print("[DEBUG] Ошибка: spliter_value <= 0")
                self.error.show_error("Ошибка: шаг точек должен быть больше 0")
                return
        except ValueError:
            print("[DEBUG] Ошибка преобразования spliter_value")
            self.error.show_error("Ошибка: некорректное значение шага точек")
            return

        # Обработка файлов
        gradient_param = self.pop_menu.magnitude_menu.get() or 'I'
        filter_type = self.pop_menu.magnitude_menu_filter.get() or 'All'
        print(f"[DEBUG] Параметры облака: gradient_param={gradient_param}, filter_type={filter_type}, "
              f"custom_min={custom_min}, custom_max={custom_max}, size_value={size_value}, spliter_value={spliter_value}")
        for i, file_name in enumerate(self.file_names[:visible_layers]):
            file_path = os.path.join(LOGS_DIR, file_name)
            if os.stat(file_path).st_size == 0:
                print(f"[DEBUG] Пустой файл: {file_name}")
                empty_files.append(file_name)
                continue

            print(f"[DEBUG] Обработка файла: {file_name}")
            result = get_result(
                file_path,
                self.node,
                gradient_param,
                custom_min,
                custom_max,
                filter_type,
                size_value,
                spliter_value,
                self.poit_mode,
            )
            if isinstance(result, NodePath):
                print(f"[DEBUG] Добавлено облако для {file_name}: node_path={result}")
                self.point_cloud_nodes.append(result)
            else:
                print(f"[DEBUG] Не удалось создать облако для {file_name}")
                error_messages.append(f"Не удалось создать облако точек для {file_name}")

        if empty_files:
            self.error.show_error(f"Пустые файлы: {', '.join(empty_files)}")
        if error_messages:
            self.error.show_error("\n".join(error_messages))

    def setup(self):
        self.node.hide()

    def show_fields(self):
        self.buttons.open_left_panel_button.show()
        self.help_text.help_text_top.show()
        self.help_text.help_text_bottom.show()
        self.help_text.alt_cam.show()
        self.input.number_input_top.show()
        self.input.number_input_bottom.show()
        self.image.image_label.show()
        self.slider.slider.show()
        self.help_text.slider_left_time.show()
        self.help_text.slider_right_time.show()

    def show(self, file_names=None, left_data_for_slider=None, right_data_for_slider=None):
        super().show()
        self.buttons.back_button_from_point.show()
        if left_data_for_slider is not None and right_data_for_slider is not None:
            self.init_text(left_data_for_slider, right_data_for_slider)
        else:
            self.left_time_slider = "1970-01-01 00:00"
            self.right_time_slider = "1970-01-01 01:00"  # Установлен диапазон по умолчанию
            self.update_slider_text()
        self.show_fields()
        if file_names:
            self.file_names = file_names
        all_data = []
        if self.file_names:
            gradient_param = self.pop_menu.magnitude_menu.get() or 'I'
            filter_type = self.pop_menu.magnitude_menu_filter.get() or "All"
            point = self.poit_mode
            print(f"[DEBUG] Инициализация облаков для файлов: gradient_param={gradient_param}, filter_type={filter_type}")
            for i in self.file_names:
                file_path = os.path.join(LOGS_DIR, i)
                if not os.stat(file_path).st_size == 0:
                    print(f"[DEBUG] Инициализация облака для {i}")
                    node_path, _, _, data = load_logs_and_create_point_cloud(
                        file_path,
                        self.node,
                        gradient_param=gradient_param,
                        filter_type=filter_type,
                        point=point,
                    )
                    if data:
                        all_data.extend(data)
                        self.point_cloud_nodes.append(node_path)

            if all_data:
                self.center_node = calculate_center(all_data)
                self.init_camera()
                self.all_data_point = all_data
                self.update_layers()

    def init_camera(self):
        """Создаёт камеру после загрузки данных."""
        if not self.camera_control:
            self.camera_control = CameraControl(self.base, self.center_node, self.help_text.alt_cam)

    def init_text(self, left_data_for_slider, right_data_for_slider):
        try:
            if isinstance(left_data_for_slider, datetime):
                self.left_time_slider = left_data_for_slider.strftime('%Y-%m-%d %H:%M')
            else:
                left_dt = datetime.strptime(str(left_data_for_slider), '%Y-%m-%d %H:%M:%S')
                self.left_time_slider = left_dt.strftime('%Y-%m-%d %H:%M')

            if isinstance(right_data_for_slider, datetime):
                self.right_time_slider = right_data_for_slider.strftime('%Y-%m-%d %H:%M')
            else:
                right_dt = datetime.strptime(str(right_data_for_slider), '%Y-%m-%d %H:%M:%S')
                self.right_time_slider = right_dt.strftime('%Y-%m-%d %H:%M')

            # Проверка совпадения времени
            left_dt = datetime.strptime(self.left_time_slider, '%Y-%m-%d %H:%M')
            right_dt = datetime.strptime(self.right_time_slider, '%Y-%m-%d %H:%M')
            if left_dt >= right_dt:
                print("[DEBUG] Совпадение начального и конечного времени, увеличение right_time на 1 час")
                right_dt = left_dt + timedelta(hours=1)
                self.right_time_slider = right_dt.strftime('%Y-%m-%d %H:%M')

            self.update_slider_text()
        except ValueError as e:
            print(f"[DEBUG] Ошибка инициализации времени: {e}")
            self.left_time_slider = "1970-01-01 00:00"
            self.right_time_slider = "1970-01-01 01:00"
            self.update_slider_text()
            self.error.show_error(f"Ошибка формата времени: {e}")

    def update_slider_text(self):
        """Обновляет текст в элементах интерфейса HelpTextUI."""
        left_dt = self.left_time_slider
        right_dt = self.right_time_slider
        self.help_text.slider_left_time['text'] = f"{left_dt}"
        self.help_text.slider_right_time['text'] = f"{right_dt}"
        print(f"[DEBUG] Обновлены метки слайдера: left={left_dt}, right={right_dt}")