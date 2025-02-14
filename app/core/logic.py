import os
import threading
from datetime import datetime

from direct.gui.DirectCheckButton import DirectCheckButton
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectOptionMenu import DGG
from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath

from app.core.UI_control.help_text import TextUI
from app.core.UI_control.slider import SliderUI
from app.core.calendar_control.calendar_app import CalendarApp
from app.core.camera_control.camera import CameraControl
from app.core.tools.const import LOGS_DIR
from app.core.config import Config
from app.core.UI_control.variables import Variables
from app.core.UI_control.buttons import ButtonsUI
from app.core.UI_control.error import ErrorDialogsUI
from app.core.UI_control.frame import FramesUI
from app.core.UI_control.image import ImageUI
from app.core.UI_control.input_fields import InputFieldsUI
from app.core.UI_control.pop_menu import PopMenuUI
from app.core.splash_screen_control.screen_saver_logic import SplashScreenLogic
from app.core.tools.utils import extract_prog_number, on_date_selected, load_logs_and_create_point_cloud, get_result, \
    calculate_center


class LogicApp(
    ShowBase,
    Variables,
    CameraControl,
    FramesUI,
    InputFieldsUI,
    ButtonsUI,
    ErrorDialogsUI,
    ImageUI,
    PopMenuUI,
    SplashScreenLogic
):
    def __init__(self):
        ShowBase.__init__(self)
        self.config = Config()
        self.setBackgroundColor(0, 0, 0)
        SplashScreenLogic.__init__(self, self, self.config)
        FramesUI.__init__(self, self.config)
        InputFieldsUI.__init__(self, self, self.config)
        ButtonsUI.__init__(self, self, self.config)
        ErrorDialogsUI.__init__(self, self, self.config)
        ImageUI.__init__(self, self.config)
        InputFieldsUI.__init__(self, self, self.config)
        PopMenuUI.__init__(self, self, self.config)
        Variables.__init__(self)
        SliderUI.__init__(self, self)
        TextUI.__init__(self, self, self.config)
        self.calendar_app = CalendarApp(self.config)
        self.help_button.bind(DGG.ENTER, self.show_hover)
        self.help_button.bind(DGG.EXIT, self.hide_hover)

    def on_date_confirmed(self):
        """Обработчик подтверждения выбора дат."""
        start_date = str(self.calendar_app.logic.start_date)
        end_date = str(self.calendar_app.logic.end_date)
        if on_date_selected(start_date, end_date) == 1:
            self.show_error_dialog()
            self.calendar_app.ui.frame.hide()
            self.calendar_app.ui.open_calendar_first.hide()
            self.calendar_app.ui.open_calendar_second.hide()
            self.confirm_button.hide()
        else:
            self.calendar_app.ui.frame.hide()
            self.calendar_app.ui.open_calendar_first.hide()
            self.calendar_app.ui.open_calendar_second.hide()
            self.start_frame.hide()
            self.date_frame.show()
            self.scroll_frame.show()
            self.calendar_app.ui.start_help_text.hide()
            self.save_data_h = start_date
            self.save_data_l = end_date
            self.load_file_list(start_date=start_date, end_date=end_date)

    def on_back_button_pressed(self):
        """Вернуться на предыдущий экран."""
        for checkbox in self.checkboxes:
            checkbox.destroy()
        self.checkboxes.clear()

        for label in self.labels:
            label.destroy()
        self.labels.clear()
        self.calendar_app.ui.start_help_text.show()
        self.calendar_app.ui.open_calendar_first.show()
        self.calendar_app.ui.open_calendar_second.show()
        self.date_frame.hide()
        self.scroll_frame.hide()
        self.start_frame.show()

    def on_checkbox_toggled(self, value, index):
        """Обработчик переключения чекбоксов."""
        file_name = self.labels[index]['text']
        if value and file_name not in self.file_names:
            self.file_names.append(file_name)
        elif not value and file_name in self.file_names:
            self.file_names.remove(file_name)
        print(f"Выбранные файлы: {self.file_names}")

    def load_file_list(self, start_date=None, end_date=None):
        """Загрузить список файлов в скроллируемый фрейм."""
        self.save_camera_allowed = False
        file_names = [
            filename for filename in os.listdir(LOGS_DIR)
            if filename.endswith('.dt') and self.filter_by_date(filename, start_date, end_date)
        ]
        file_names.sort(key=lambda x: int(x.split('_')[0].replace('prog', '')))

        element_height = 0.1
        total_height = len(file_names) * element_height
        self.scroll_frame['canvasSize'] = (-0.9, 0.9, -total_height, 0.1)

        for i, file_name in enumerate(file_names):
            y_pos = -0.03 - i * element_height
            y_poz_for_check = -0.01 - i * element_height
            label = DirectLabel(
                text=file_name, scale=0.07, pos=(-0.3, 0, y_pos),
                parent=self.scroll_frame.getCanvas(), frameColor=(0, 0, 0, 0),
            )
            self.labels.append(label)
            checkbox = DirectCheckButton(
                scale=0.05, pos=(0.8, 0, y_poz_for_check), parent=self.scroll_frame.getCanvas(),
                indicatorValue=0, command=self.on_checkbox_toggled, extraArgs=[i],
                relief=None,
            )
            self.checkboxes.append(checkbox)

    def select_all_up(self):
        """Выделяет или очищает все чекбоксы."""
        all_selected = all(cb["indicatorValue"] for cb in self.checkboxes)
        new_state = 0 if all_selected else 1

        self.file_names.clear()  # Очищаем список перед выбором

        for i, checkbox in enumerate(self.checkboxes):
            checkbox["indicatorValue"] = new_state
            checkbox.setIndicatorValue()
            self.on_checkbox_toggled(new_state, i)  # Вызываем обработчик, как при клике

        # Меняем текст кнопки
        self.select_all_up["text"] = "Очистить все" if new_state else "Выбрать все"

    @staticmethod
    def filter_by_date(filename, start_date, end_date):
        """Фильтровать файлы по диапазону дат."""
        prog_number, file_date = extract_prog_number(filename)
        if start_date and end_date:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            return start_date_obj <= file_date <= end_date_obj
        return True

    def on_done_button_pressed(self):
        """Обработчик кнопки 'Готово'."""
        if len(self.file_names) == 0:
            self.show_error_empty_log()
        else:
            self.date_frame.hide()
            self.scroll_frame.hide()
            print(f"Выбранные файлы: {self.file_names}")

        self.point_cloud_nodes = []
        all_points = []  # Список для хранения всех точек

        gradient_param = self.magnitude_menu.get()
        filter_type = self.magnitude_menu.get()  # Получаем выбранный фильтр

        for i, file_name in enumerate(self.file_names):
            file_path = os.path.join(LOGS_DIR, file_name)
            node_path = load_logs_and_create_point_cloud(
                file_path, self.render,
                gradient_param=gradient_param,
                filter_type=filter_type
            )

            if node_path:
                print(f"Файл {file_name}: облако точек добавлено.")
                self.point_cloud_nodes.append(node_path)
                self.info_frame.show()

                # Добавляем точки из текущего файла в общий список
                if isinstance(node_path, tuple):
                    points = node_path[-1]  # Предполагаем, что точки находятся в последнем элементе кортежа
                    all_points.extend(points)

        # Вычисляем центр для всех точек
        if all_points:
            Variables.center = calculate_center(all_points)
            print(f"[DEBUG] Центр всех точек: {Variables.center}")

        if self.point_cloud_nodes:
            self.back_button_from_point_view.show()
            self.image_label.show()
            self.number_input_top.show()
            self.number_input_bottom.show()
            self.save_camera_allowed = True
            if self.save_camera_allowed:
                CameraControl.__init__(self, self)
            print("Позиция камеры установлена вручную.")

    def refresh_gradient(self):
        """Перерисовать облака точек с новым параметром градиента и учётом слайдера."""
        self.saved_gradient_param = self.magnitude_menu.get()
        self.saved_filter_type = self.magnitude_menu_filter.get()

        try:
            self.saved_min = float(self.number_input_bottom.get())
            self.saved_max = float(self.number_input_top.get())
        except ValueError:
            print("Ошибка: некорректные значения в полях ввода.")
            return

        if self.saved_min >= self.saved_max:
            self.error_min_max.show()
            return

        slider_value = self.slider.getValue()
        visible_layers = int((slider_value / 100) * len(self.file_names))

        print(f"Обновление градиента и слоев: {self.saved_gradient_param}, отображаем 0-{visible_layers - 1} слоев.")

        self.clear_point_cloud_nodes()
        self.update_point_cloud_nodes(visible_layers)

        print(f"Обновление завершено: {len(self.point_cloud_nodes)} облаков точек перерисовано.")

    def back_from_point_view(self):
        for node in self.point_cloud_nodes:
            if isinstance(node, tuple):
                node_path = node[0]
            else:
                node_path = node

            if isinstance(node_path, NodePath):
                node_path.removeNode()

        self.point_cloud_nodes.clear()
        self.file_names.clear()

        for checkbox in self.checkboxes:
            checkbox.destroy()
        self.checkboxes.clear()

        for label in self.labels:
            label.destroy()
        self.labels.clear()
        self.save_camera_allowed = False
        self.disable_camera_control()
        self.back_button_from_point_view.hide()
        self.back_button.show()
        self.image_label.hide()
        self.info_frame.hide()
        self.number_input_top.hide()
        self.number_input_bottom.hide()
        self.date_frame.show()
        self.select_all_up["text"] = 'Выбрать все'
        self.scroll_frame.show()
        self.load_file_list(self.save_data_h, self.save_data_l)

    def on_slider_change(self):
        """Обработчик изменения слайдера для управления слоями."""
        slider_value = self.slider['value']

        if self.slider_timer is not None:
            self.slider_timer.cancel()

        self.slider_timer = threading.Timer(1.0, self.update_layers, args=(slider_value,))
        self.slider_timer.start()

    def update_layers(self, slider_value):
        """Обновляет отображаемые слои на основе значения слайдера."""
        visible_layers = int((slider_value / 100) * len(self.file_names))
        print(f"Обновление слоев: отображаем 0-{visible_layers - 1} слоев.")

        self.clear_point_cloud_nodes()
        self.update_point_cloud_nodes(visible_layers)

        print(f"Отображается {len(self.point_cloud_nodes)} слоев.")

    def close_error_dialog(self, _):
        """Закрыть диалог ошибки."""
        if hasattr(self, 'error_dialog'):
            self.error_dialog.hide()
            self.calendar_app.ui.open_calendar_first.show()
            self.calendar_app.ui.open_calendar_second.show()
            self.confirm_button.show()

    def show_error_dialog(self):
        """Показать диалог ошибки."""
        self.error_dialog.show()

    def show_error_min_max(self):
        """Показать диалог ошибки."""
        self.error_min_max.show()

    def show_error_empty_log(self):
        """Показать диалог ошибки."""
        self.error_empty_log.show()

    def close_error_min_max(self, _):
        """Закрыть диалог ошибки."""
        if hasattr(self, 'error_dialog'):
            self.error_min_max.hide()

    def close_error_empty_log(self, _):
        """Закрыть диалог ошибки."""
        if hasattr(self, 'error_dialog'):
            self.error_empty_log.hide()

    def update_labels(self, selected_item):
        if selected_item == "I":
            self.parameters_up_help["text"] = "I max"
            self.parameters_down_help["text"] = "I min"
        elif selected_item == "U":
            self.parameters_up_help["text"] = "U max"
            self.parameters_down_help["text"] = "U min"
        elif selected_item == "WFS":
            self.parameters_up_help["text"] = "WFS max"
            self.parameters_down_help["text"] = "WFS min"

    def disable_camera_control(self):
        """Отключает управление камерой."""
        self.taskMgr.remove("UpdateCameraTask")
        self.ignore("mouse1")  # Игнорируем ЛКМ
        self.ignore("mouse3")  # Игнорируем ПКМ
        self.ignore("wheel_up")  # Игнорируем прокрутку вверх
        self.ignore("wheel_down")

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

    def update_point_cloud_nodes(self, visible_layers):
        """Обновляет облака точек на основе видимых слоев и текущих параметров."""
        for i, file_name in enumerate(self.file_names[:visible_layers]):
            result = get_result(
                os.path.join(LOGS_DIR, file_name),
                self.render,
                self.saved_gradient_param,
                self.saved_min,
                self.saved_max,
                self.saved_filter_type,
                float(self.size_input.get()),
                self.spliter_input.get()
            )

            if isinstance(result, NodePath):
                self.point_cloud_nodes.append(result)

    def show_hover(self, event):
        self.hover_label.show()

    def hide_hover(self, event):
        self.hover_label.hide()
