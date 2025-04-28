import os
import threading
from datetime import datetime, timedelta

from panda3d.core import NodePath

from app_ref.Scene4.ButtonUI import ButtonsUI
from app_ref.Scene4.FrameUI import FramesUI
from app_ref.Scene4.HelpTextUI import HelpTextUI
from app_ref.Scene4.ImageUI import ImageUI
from app_ref.Scene4.InputUI import InputUI
from app_ref.Scene4.PopUi import PopMenuUI
from app_ref.Scene4.SliderUI import SliderUI
from app_ref.Scene4.error import ErrorDialogsUI
from app_ref.Scene4.utils import load_logs_and_create_point_cloud, calculate_center, get_result, \
    get_gradient_param_values, load_log_data
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
        self.base.accept('enter', self.update_layers)

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
        """Handle UI parameter changes."""
        self.update_layers()

    def clear_point_cloud_nodes(self):
        """Clear all current point cloud nodes."""
        for node in self.point_cloud_nodes:
            node_path = node[0] if isinstance(node, tuple) else node
            if isinstance(node_path, NodePath):
                node_path.removeNode()
        self.point_cloud_nodes.clear()

    def on_back_button_from_point(self):
        """Hide scene elements, clear data, and switch to Scene3 with file names."""
        try:
            self.hide_fields()
            self.node.hide()
            self.clear_point_cloud_nodes()
            if self.camera_control:
                self.camera_control.deactivate()
            self.file_names = []
            self.all_data_point = []
            self.left_time_slider = 0
            self.right_time_slider = 0
            self.update_slider_text()
            self.switch_callback(3)
        except Exception as e:
            self.error.show_error_dialog(f"Ошибка возврата на Scene3: {e}")

    def hide_fields(self):
        """Hide all UI fields."""
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
                pass

    def on_slider_change(self):
        """Handle slider changes for layer updates."""
        if not self.file_names:
            return
        slider_value = self.slider.slider['value']
        if self.slider_timer is not None:
            self.slider_timer.cancel()
        self.slider_timer = threading.Timer(0.5, self.update_layers, args=(slider_value,))
        self.slider_timer.start()

    def update_layers(self, slider_value=None):
        """Update displayed layers based on slider position."""
        if slider_value is None:
            slider_value = self.slider.slider['value']

        if not self.file_names:
            return

        if not self._validate_time_range():
            return

        visible_layers = int((slider_value / 100) * len(self.file_names))
        self.clear_point_cloud_nodes()
        self.update_point_cloud_nodes(visible_layers)

    def _validate_time_range(self):
        """Validate the time range for slider."""
        try:
            left_dt = datetime.strptime(self.left_time_slider, '%Y-%m-%d %H:%M')
            right_dt = datetime.strptime(self.right_time_slider, '%Y-%m-%d %H:%M')
            if (right_dt - left_dt).total_seconds() <= 0:
                self.error.show_error_dialog("Ошибка: конечное время должно быть позже начального.")
                return False
        except ValueError as e:
            self.error.show_error_dialog(f"Ошибка формата времени: {e}")
            return False
        return True

    def update_point_cloud_nodes(self, visible_layers):
        """Update point clouds for the specified number of layers."""
        params = self._validate_and_get_params()
        if not params:
            return

        empty_files, error_messages = self._process_files_for_layers(visible_layers, params)

        if empty_files:
            self.error.show_error_dialog(f"Пустые файлы: {', '.join(empty_files)}")
        if error_messages:
            self.error.show_error_dialog("\n".join(error_messages))

    def _validate_and_get_params(self):
        try:
            custom_min = float(self.input.number_input_bottom.get()) if self.input.number_input_bottom.get() else None
            custom_max = float(self.input.number_input_top.get()) if self.input.number_input_top.get() else None
            if custom_min is not None and custom_max is not None and custom_min >= custom_max:
                self.error.show_error_dialog("Ошибка: custom_min должен быть меньше custom_max")
                return None
        except ValueError:
            self.error.show_error_dialog("Ошибка: введены некорректные значения min/max")
            return None

        try:
            size_value = float(self.input.size_input.get()) if self.input.size_input.get() else 1.0
            if size_value <= 0:
                self.error.show_error_dialog("Ошибка: размер точки должен быть больше 0")
                return None
        except ValueError:
            self.error.show_error_dialog("Ошибка: некорректное значение размера точки")
            return None

        try:
            spliter_value = float(self.input.spliter_input.get()) if self.input.spliter_input.get() else 1
            if spliter_value <= 0:
                self.error.show_error_dialog("Ошибка: шаг точек должен быть больше 0")
                return None
        except ValueError:
            self.error.show_error_dialog("Ошибка: некорректное значение шага точек")
            return None

        filter_mapping = {
            "Все точки": "all",
            "Внутри диапазона": "inside",
            "За диап.": "outside"
        }
        filter_type = filter_mapping.get(self.pop_menu.magnitude_menu_filter.get(), "all")

        return {
            'gradient_param': self.pop_menu.magnitude_menu.get(),
            'filter_type': filter_type,
            'custom_min': custom_min,
            'custom_max': custom_max,
            'size_value': size_value,
            'spliter_value': spliter_value
        }

    def _process_files_for_layers(self, visible_layers, params):
        """Process files to create point clouds for the specified layers."""
        empty_files = []
        error_messages = []

        print(f"[DEBUG] Processing {visible_layers} files with params: {params}")

        for file_path in self.file_names[:visible_layers]:
            print(f"[DEBUG] Processing file: {file_path}")
            try:
                if os.stat(file_path).st_size == 0:
                    empty_files.append(os.path.basename(file_path))
                    print(f"[DEBUG] File {file_path} is empty")
                    continue
            except OSError as e:
                error_messages.append(f"Ошибка доступа к файлу {os.path.basename(file_path)}: {e}")
                print(f"[DEBUG] OSError for file {file_path}: {e}")
                continue

            try:
                data, i_values, u_values, wfs_values, gi7_values, gi8_values, gi9_values, gi10_values, motor_current_values = load_log_data(
                    file_path)
                if not data:
                    print(f"[DEBUG] No data in file {file_path}")
                    continue

                param_values = get_gradient_param_values(
                    params['gradient_param'], i_values, u_values, wfs_values,
                    gi7_values, gi8_values, gi9_values, gi10_values, motor_current_values
                )
                if param_values is None:
                    error_messages.append(f"Не удалось получить значения параметра для {os.path.basename(file_path)}")
                    print(f"[DEBUG] param_values is None for {file_path}")
                    continue

                min_val, max_val = min(param_values), max(param_values)
                print(f"[DEBUG] Data range for {file_path}: min={min_val}, max={max_val}")

                if params['filter_type'] == "outside" and params['custom_min'] is not None and params[
                    'custom_max'] is not None:
                    if min_val >= params['custom_min'] and max_val <= params['custom_max']:
                        print(
                            f"[DEBUG] All points in {file_path} are inside range [{params['custom_min']}, {params['custom_max']}]. Skipping.")
                        continue

                result = get_result(
                    file_path,
                    self.node,
                    params['gradient_param'],
                    params['custom_min'],
                    params['custom_max'],
                    params['filter_type'],
                    params['size_value'],
                    params['spliter_value'],
                    self.poit_mode,
                )
                print(f"[DEBUG] get_result returned: {type(result)}")
                if isinstance(result, NodePath):
                    self.point_cloud_nodes.append(result)
                else:
                    continue
            except Exception as e:
                error_messages.append(f"Ошибка обработки файла {os.path.basename(file_path)}: {e}")

        # Combine messages and show only if necessary
        all_messages = []
        if empty_files:
            all_messages.append(f"Пустые файлы: {', '.join(empty_files)}")
        if error_messages:
            all_messages.extend(error_messages)

        if all_messages:
            # Show error dialog only once with all messages
            self.error.show_error_dialog("\n".join(all_messages))

        return empty_files, error_messages

    def setup(self):
        """Hide the node during setup."""
        self.node.hide()

    def show_fields(self):
        """Show all UI fields."""
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

    def show(self, file_names=None, selected_file_names=None, left_data_for_slider=None, right_data_for_slider=None):
        """Show the scene with the specified files and slider times."""
        super().show()
        self.ui_node.show()
        self.buttons.open_left_panel_button.show()
        if self.camera_control:
            self.camera_control.activate()
        self.buttons.back_button_from_point.show()

        self._init_slider_text(left_data_for_slider, right_data_for_slider)
        self.clear_point_cloud_nodes()

        if not file_names:
            self.error.show_error_dialog("Ошибка: не выбраны файлы для отображения")
            self.show_fields()
            return

        valid_files = self._validate_and_store_files(file_names)
        if not valid_files:
            self.show_fields()
            return

        self.selected_files = selected_file_names if selected_file_names else []

        all_data = self._process_files_for_point_clouds()
        if all_data:
            self._initialize_scene(all_data)
        else:
            self.error.show_error_dialog("Ошибка: нет данных для отображения облаков точек")

        self.show_fields()

    def _init_slider_text(self, left_data, right_data):
        """Initialize slider text with provided or default times."""
        if left_data is not None and right_data is not None:
            self.init_text(left_data, right_data)
        else:
            self.left_time_slider = "1970-01-01 00:00"
            self.right_time_slider = "1970-01-01 01:00"
            self.update_slider_text()

    def _validate_and_store_files(self, file_names):
        """Validate and store file paths, reporting missing files."""
        if isinstance(file_names, (tuple, set)):
            file_names = list(file_names)
        elif isinstance(file_names, str):
            file_names = [file_names]

        self.file_names = []
        missing_files = []

        for file_path in file_names:
            if not os.path.exists(file_path):
                missing_files.append(os.path.basename(file_path))
            else:
                self.file_names.append(file_path)

        if missing_files:
            self.error.show_error_dialog(f"Файлы не найдены: {', '.join(missing_files)}")

        return self.file_names

    def _process_files_for_point_clouds(self):
        """Process files to create initial point clouds."""
        all_data = []
        empty_files = []
        error_messages = []

        gradient_param = self.pop_menu.magnitude_menu.get()
        filter_type = self.pop_menu.magnitude_menu_filter.get()

        filter_mapping = {
            "Все точки": "all",
            "Внутри диапазона": "inside",
            "За диап.": "outside"
        }
        filter_type = filter_mapping.get(filter_type, "all")

        custom_min = float(self.input.number_input_bottom.get()) if self.input.number_input_bottom.get() else None
        custom_max = float(self.input.number_input_top.get()) if self.input.number_input_top.get() else None

        for file_path in self.file_names:
            try:
                if os.stat(file_path).st_size == 0:
                    empty_files.append(os.path.basename(file_path))
                    continue
            except OSError:
                continue

            try:
                data, i_values, u_values, wfs_values, gi7_values, gi8_values, gi9_values, gi10_values, motor_current_values = load_log_data(
                    file_path)
                if not data:
                    continue

                param_values = get_gradient_param_values(
                    gradient_param, i_values, u_values, wfs_values,
                    gi7_values, gi8_values, gi9_values, gi10_values, motor_current_values
                )
                if param_values is None:
                    continue

                min_val, max_val = min(param_values), max(param_values)
                print(f"[DEBUG] Data range for {file_path}: min={min_val}, max={max_val}")

                node_path, _, _, data = load_logs_and_create_point_cloud(
                    file_path,
                    self.node,
                    gradient_param=gradient_param,
                    filter_type=filter_type,
                    point=self.poit_mode,
                    custom_min=custom_min,
                    custom_max=custom_max,
                )
                if data:
                    all_data.extend(data)
                    self.point_cloud_nodes.append(node_path)
                else:
                    print(f"[DEBUG] No points after filtering for {file_path}. Skipping.")
            except Exception as e:
                error_messages.append(f"Ошибка обработки файла {os.path.basename(file_path)}: {e}")

        all_messages = []
        if empty_files:
            all_messages.append(f"Пустые файлы: {', '.join(empty_files)}")
        if error_messages:
            all_messages.extend(error_messages)

        if all_messages:
            self.error.show_error_dialog("\n".join(all_messages))

        return all_data

    def _initialize_scene(self, all_data):
        """Initialize the scene with point cloud data."""
        self.center_node = calculate_center(all_data)
        self.init_camera()
        self.all_data_point = all_data
        self.update_layers()

    def init_camera(self):
        """Initialize the camera after loading data."""
        if not self.camera_control:
            self.camera_control = CameraControl(self.base, self.center_node, self.help_text.alt_cam)

    def init_text(self, left_data_for_slider, right_data_for_slider):
        """Initialize slider text with provided times."""
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

            left_dt = datetime.strptime(self.left_time_slider, '%Y-%m-%d %H:%M')
            right_dt = datetime.strptime(self.right_time_slider, '%Y-%m-%d %H:%M')
            if left_dt >= right_dt:
                right_dt = left_dt + timedelta(hours=1)
                self.right_time_slider = right_dt.strftime('%Y-%m-%d %H:%M')

            self.update_slider_text()
        except ValueError as e:
            self.left_time_slider = "1970-01-01 00:00"
            self.right_time_slider = "1970-01-01 01:00"
            self.update_slider_text()
            self.error.show_error_dialog(f"Ошибка формата времени: {e}")

    def update_slider_text(self):
        """Update slider text in UI."""
        self.help_text.slider_left_time['text'] = f"{self.left_time_slider}"
        self.help_text.slider_right_time['text'] = f"{self.right_time_slider}"