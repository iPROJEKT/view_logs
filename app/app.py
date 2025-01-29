import os
import threading
from datetime import datetime

from direct.gui.DirectCheckButton import DirectCheckButton
from direct.gui.DirectDialog import OkDialog
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectOptionMenu import DirectOptionMenu
from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import NodePath

from app.camera import CameraControl
from app.const import LOGS_DIR, YEARS, MONTHS, DAYS
from app.init_app import MyAppInit
from app.utils import extract_prog_number, on_date_selected, load_logs_and_create_point_cloud


class MyApp(ShowBase, MyAppInit, CameraControl):
    def __init__(self):
        ShowBase.__init__(self)
        MyAppInit.__init__(self)
        CameraControl.__init__(self, self)

    def create_date_selectors(self, y_offset, font):
        """Создать элементы выбора даты."""
        year_menu = DirectOptionMenu(
            text="Год", scale=0.09, items=YEARS, initialitem=len(YEARS) - 1,
            pos=(-0.6, 0, y_offset), text_font=font, parent=self.start_frame
        )
        month_menu = DirectOptionMenu(
            text="Месяц", scale=0.09, items=MONTHS, initialitem=datetime.now().month - 1,
            pos=(-0.2, 0, y_offset), text_font=font, parent=self.start_frame
        )
        day_menu = DirectOptionMenu(
            text="День", scale=0.09, items=DAYS, initialitem=datetime.now().day - 1,
            pos=(0.1, 0, y_offset), text_font=font, parent=self.start_frame
        )
        return year_menu, month_menu, day_menu

    def load_file_list(self, start_date=None, end_date=None):
        """Загрузить список файлов в скроллируемый фрейм."""
        file_names = [
            filename for filename in os.listdir(LOGS_DIR)
            if filename.endswith('.dt') and self.filter_by_date(filename, start_date, end_date)
        ]
        file_names.sort(key=lambda x: int(x.split('_')[0].replace('prog', '')))

        element_height = 0.1
        total_height = len(file_names) * element_height
        self.scroll_frame['canvasSize'] = (-0.9, 0.9, -total_height, 0.1)

        for i, file_name in enumerate(file_names):
            y_pos = -0.02 - i * element_height
            label = DirectLabel(
                text=file_name, scale=0.05, pos=(-0.5, 0, y_pos),
                parent=self.scroll_frame.getCanvas(), frameColor=(0, 0, 0, 0)
            )
            self.labels.append(label)
            checkbox = DirectCheckButton(
                scale=0.05, pos=(0.5, 0, y_pos), parent=self.scroll_frame.getCanvas(),
                indicatorValue=0, command=self.on_checkbox_toggled, extraArgs=[i]
            )
            self.checkboxes.append(checkbox)

    def filter_by_date(self, filename, start_date, end_date):
        """Фильтровать файлы по диапазону дат."""
        prog_number, file_date = extract_prog_number(filename)
        if start_date and end_date:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            return start_date_obj <= file_date <= end_date_obj
        return True

    def on_checkbox_toggled(self, value, index):
        """Обработчик переключения чекбоксов."""
        file_name = self.labels[index]['text']
        if value and file_name not in self.file_names:
            self.file_names.append(file_name)
        elif not value and file_name in self.file_names:
            self.file_names.remove(file_name)
        print(f"Выбранные файлы: {self.file_names}")

    def on_date_confirmed(self):
        """Обработчик подтверждения выбора дат."""
        start_date = f"{self.year_menu_first.get()}-{self.month_menu_first.get().zfill(2)}-{self.day_menu_first.get().zfill(2)}"
        end_date = f"{self.year_menu_second.get()}-{self.month_menu_second.get().zfill(2)}-{self.day_menu_second.get().zfill(2)}"

        if on_date_selected(start_date, end_date) == 1:
            self.show_error_dialog()
        else:
            self.start_frame.hide()
            self.date_frame.show()
            self.scroll_frame.show()
            self.load_file_list(start_date=start_date, end_date=end_date)

    def show_error_dialog(self):
        """Показать диалог ошибки."""
        self.error_dialog = OkDialog(
            dialogName="ErrorDialog", text="Ошибка: конечная дата должна быть позже начальной!",
            buttonTextList=["OK"], command=self.close_error_dialog
        )

    def close_error_dialog(self, _):
        """Закрыть диалог ошибки."""
        if hasattr(self, 'error_dialog'):
            self.error_dialog.destroy()

    def on_back_button_pressed(self):
        """Вернуться на предыдущий экран."""
        for checkbox in self.checkboxes:
            checkbox.destroy()
        self.checkboxes.clear()

        for label in self.labels:
            label.destroy()
        self.labels.clear()

        self.date_frame.hide()
        self.scroll_frame.hide()
        self.start_frame.show()

    def on_done_button_pressed(self):
        """Обработчик кнопки 'Готово'."""
        self.date_frame.hide()
        self.scroll_frame.hide()
        print(f"Выбранные файлы: {self.file_names}")

        if hasattr(self, 'point_cloud_nodes'):
            for node in self.point_cloud_nodes:
                node.removeNode()
        self.point_cloud_nodes = []

        gradient_param = self.magnitude_menu.get()
        filter_type = self.magnitude_menu.get()  # Получаем выбранный фильтр

        for i, file_name in enumerate(self.file_names):
            file_path = os.path.join(LOGS_DIR, file_name)
            node_path = load_logs_and_create_point_cloud(
                file_path, self.render, gradient_param=gradient_param, filter_type=filter_type
            )

            if node_path:
                print(f"Файл {file_name}: облако точек добавлено.")
                self.point_cloud_nodes.append(node_path)
                self.info_frame.show()

        if self.point_cloud_nodes:
            self.image_label.show()
            self.number_input_top.show()
            self.number_input_bottom.show()
            print("Позиция камеры установлена вручную.")

    def refresh_gradient(self):
        """Перерисовать облака точек с новым параметром градиента."""
        # Сохраняем текущие значения фильтров и полей ввода
        self.saved_gradient_param = self.magnitude_menu.get()
        self.saved_filter_type = self.magnitude_menu_filter.get()
        try:
            self.saved_min = float(self.number_input_bottom.get())
            self.saved_max = float(self.number_input_top.get())
        except ValueError:
            print("Ошибка: некорректные значения в полях ввода.")
            return

        # Удаляем старые облака точек
        for node in self.point_cloud_nodes:
            if isinstance(node, tuple):
                node_path = node[0]
            else:
                node_path = node

            if isinstance(node_path, NodePath):
                node_path.removeNode()

        self.point_cloud_nodes.clear()

        for file_name in self.file_names:
            file_path = os.path.join(LOGS_DIR, file_name)
            result = load_logs_and_create_point_cloud(
                file_path=file_path,
                parent=self.render,
                gradient_param=self.saved_gradient_param,
                custom_min=self.saved_min,
                custom_max=self.saved_max,
                filter_type=self.saved_filter_type
            )

            if result:
                if isinstance(result, tuple):
                    node_path = result[0]
                else:
                    node_path = result

                if isinstance(node_path, NodePath):
                    self.point_cloud_nodes.append(node_path)

        print(f"Обновление завершено: {len(self.point_cloud_nodes)} облаков точек перерисовано.")

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
        for node in self.point_cloud_nodes:
            if isinstance(node, tuple):
                node_path = node[0]
            else:
                node_path = node

            if isinstance(node_path, NodePath):
                node_path.removeNode()

        self.point_cloud_nodes.clear()

        for i, file_name in enumerate(self.file_names[:visible_layers]):
            file_path = os.path.join(LOGS_DIR, file_name)
            result = load_logs_and_create_point_cloud(
                file_path=file_path,
                parent=self.render,
                gradient_param=self.saved_gradient_param,
                custom_min=self.saved_min,
                custom_max=self.saved_max,
                filter_type=self.saved_filter_type
            )

            if result:
                if isinstance(result, tuple):
                    node_path = result[0]
                else:
                    node_path = result

                if isinstance(node_path, NodePath):
                    self.point_cloud_nodes.append(node_path)

        print(f"Отображается {len(self.point_cloud_nodes)} слоев.")
