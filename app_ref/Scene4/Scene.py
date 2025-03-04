import os
import threading
from datetime import datetime

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
        print("[DEBUG] Scene4 initialized")

    def clear_point_cloud_nodes(self):
        """Очищает все текущие облака точек."""
        for node in self.point_cloud_nodes:
            if isinstance(node, tuple):
                node_path = node[0]
            else:
                node_path = node
            if isinstance(node_path, NodePath):
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
                print("[DEBUG] Cleaning up camera control")
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
            print("[DEBUG] Scene4 hidden and cleared successfully")
            self.switch_callback(3)  # Переключаемся на Scene3
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
        if self.slider_timer is not None:
            self.slider_timer.cancel()
        self.slider_timer = threading.Timer(1.0, self.update_layers, args=(slider_value,))
        self.slider_timer.start()

    def update_layers(self, slider_value=None):
        """Обновляет отображаемые слои пропорционально положению слайдера."""
        if slider_value is None:
            slider_value = self.slider.slider['value']

        if not self.file_names or self.right_time_slider == 0 or self.left_time_slider == 0:
            return

        visible_layers = int((slider_value / 100) * len(self.file_names))
        time_range = self.right_time_slider - self.left_time_slider
        current_time = self.left_time_slider + (slider_value / 100) * time_range
        print(f"Обновление слоев: отображаем 0-{visible_layers - 1} слоев.")
        print(f"Текущее время: {current_time} (из диапазона {self.left_time_slider} - {self.right_time_slider})")

        self.clear_point_cloud_nodes()
        self.update_point_cloud_nodes(visible_layers)

    def update_point_cloud_nodes(self, visible_layers):
        """Обновляет облака точек, показывая только заданное количество слоев."""
        empty_files = []
        error_messages = []

        custom_min = self.input.number_input_bottom.get()
        custom_max = self.input.number_input_top.get()
        try:
            custom_min = float(custom_min) if custom_min else None
            custom_max = float(custom_max) if custom_max else None
            if custom_min is not None and custom_max is not None and custom_min >= custom_max:
                return
        except ValueError:
            custom_min = None
            custom_max = None

        try:
            size_value = float(self.input.size_input.get()) if self.input.size_input.get() else 0
            if size_value <= 0:
                return
        except ValueError:
            return

        try:
            spliter_value = float(self.input.spliter_input.get()) if self.input.spliter_input.get() else 0
            if spliter_value <= 0:
                return
        except ValueError:
            return

        if error_messages:
            self.error.update_file_list(error_messages)
            return

        for i, file_name in enumerate(self.file_names[:visible_layers]):
            file_path = os.path.join(LOGS_DIR, file_name)
            if os.stat(file_path).st_size == 0:
                empty_files.append(file_name)
                continue

            result = get_result(
                file_path,
                self.node,
                self.pop_menu.magnitude_menu.get(),
                custom_min,
                custom_max,
                self.pop_menu.magnitude_menu_filter.get(),
                self.input.size_input.get(),
                self.input.spliter_input.get(),
                self.poit_mode
            )
            if isinstance(result, NodePath):
                self.point_cloud_nodes.append(result)

        print(f"Отображается {len(self.point_cloud_nodes)} слоев.")

    def setup(self):
        self.node.hide()

    def show_fields(self):
        print("[DEBUG] Showing fields")
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
        if left_data_for_slider is not None and right_data_for_slider is not None:  # Проверяем на None явно
            self.init_text(left_data_for_slider, right_data_for_slider)
        else:
            self.left_time_slider = 0
            self.right_time_slider = 0
            self.update_slider_text()
        self.show_fields()
        if file_names:
            self.file_names = file_names
        all_data = []
        if self.file_names:
            for i in self.file_names:
                file_path = os.path.join(LOGS_DIR, i)
                if not os.stat(file_path).st_size == 0:
                    gradient_param = 'I'
                    filter_type = "All"
                    point = True
                    node_path, _, _, data = load_logs_and_create_point_cloud(
                        file_path,
                        self.node,
                        gradient_param=gradient_param,
                        filter_type=filter_type,
                        point=point
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
            print("[DEBUG] Camera initialized")

    def init_text(self, left_data_for_slider, right_data_for_slider):
        print(f"[DEBUG] Initializing text with left={left_data_for_slider}, right={right_data_for_slider}")
        try:
            if isinstance(left_data_for_slider, datetime):
                self.left_time_slider = left_data_for_slider.timestamp()
            else:
                left_dt = datetime.strptime(str(left_data_for_slider), '%Y-%m-%d %H:%M:%S')
                self.left_time_slider = left_dt.timestamp()

            if isinstance(right_data_for_slider, datetime):
                self.right_time_slider = right_data_for_slider.timestamp()
            else:
                right_dt = datetime.strptime(str(right_data_for_slider), '%Y-%m-%d %H:%M:%S')
                self.right_time_slider = right_dt.timestamp()
            self.update_slider_text()
            print(f"[DEBUG] Slider updated: {self.left_time_slider} - {self.right_time_slider}")
        except ValueError as e:
            print(f"[DEBUG] ValueError in init_text: {e}, resetting to 0")
            self.left_time_slider = 0
            self.right_time_slider = 0
            self.update_slider_text()

    def update_slider_text(self):
        """Обновляет текст в элементах интерфейса HelpTextUI."""
        left_dt = datetime.fromtimestamp(self.left_time_slider).strftime('%H:%M')
        right_dt = datetime.fromtimestamp(self.right_time_slider).strftime('%H:%M')
        self.help_text.slider_left_time['text'] = f"{left_dt}"
        self.help_text.slider_right_time['text'] = f"{right_dt}"
        print(f"[DEBUG] Slider text set to: {left_dt} - {right_dt}")
