import os
from datetime import datetime

from direct.gui.DirectCheckButton import DirectCheckButton
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode

from app_ref.config import ConfigApp
from app.core.tools.const import LOGS_DIR
from app_ref.Sceen3.error import ErrorDialogsUI
from app_ref.Sceen3.ButtonUI import ButtonsUI
from app_ref.Sceen3.FrameUI import FramesUI
from app_ref.Sceen3.utils import extract_prog_number, filter_by_date
from app_ref.SceneABS.SceneABS import Screen


class Scene3(Screen):
    def __init__(self, name, base, switch_callback):
        super().__init__(name, base)
        self.name = name
        self.config_app = ConfigApp()
        self.save_camera_allowed = False
        self.file_names = []
        self.labels = []
        self.checkboxes = []
        self.start_date = None
        self.end_date = None
        self.left_data_for_slider = None
        self.right_data_for_slider = None

        self.ui_node = self.node.attachNewNode("UI_Scene3")
        self.frames = FramesUI(self.config_app)
        self.buttons = ButtonsUI(
            self.ui_node,
            base,
            self.config_app,
            self.frames.date_frame,
            on_done_button_select_logs_view=self.on_done_button_select_logs_view,
            on_back_button_on_calendar=self.on_back_button_on_calendar,
            select_all_up=self.select_all_up
        )
        self.error = ErrorDialogsUI(
            self.config_app,
            base,
            frame=self.frames.date_frame
        )

        self.switch_callback = switch_callback

    def _on_checkbox_toggled(self, value, index):
        """Обработчик переключения чекбоксов."""
        file_name = self.labels[index]['text']
        if value and file_name not in self.file_names:
            self.file_names.append(file_name)
        elif not value and file_name in self.file_names:
            self.file_names.remove(file_name)

    def load_file_list(self, start_date: str = None, end_date: str = None):
        """Загружает список файлов в скроллируемый фрейм с фильтрацией по дате."""
        for label in self.labels:
            label.destroy()
        for checkbox in self.checkboxes:
            checkbox.destroy()

        self.labels.clear()
        self.checkboxes.clear()
        self.file_names.clear()
        self.left_data_for_slider = None
        self.right_data_for_slider = None

        file_names = [
            f for f in os.listdir(LOGS_DIR)
            if f.lower().endswith('.dt') and filter_by_date(f, start_date, end_date)
        ]
        file_names.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
        element_height = 0.1
        total_height = len(file_names) * element_height
        self.frames.scroll_frame['canvasSize'] = (-0.9, 0.9, -total_height, 0.1)

        for i, file_name in enumerate(file_names):
            self._add_file_entry(file_name, i, element_height)

    def _add_file_entry(self, file_name: str, index: int, element_height: float):
        """Создаёт строку в списке файлов с чекбоксом."""
        y_pos = -0.03 - index * element_height
        y_pos_check = -0.01 - index * element_height
        _, file_date = extract_prog_number(file_name)
        if file_date != datetime.min:
            self._update_date_range(file_date)
        label = DirectLabel(
            text=file_name,
            text_align=TextNode.ALeft,
            scale=0.07,
            pos=(-0.75, 0, y_pos),
            parent=self.frames.scroll_frame.getCanvas(),
            frameColor=(0, 0, 0, 0),
        )
        self.labels.append(label)
        checkbox = DirectCheckButton(
            scale=0.05,
            pos=(0.8, 0, y_pos_check),
            parent=self.frames.scroll_frame.getCanvas(),
            indicatorValue=0,
            command=self._on_checkbox_toggled,
            extraArgs=[index],
            relief=None,
        )
        self.checkboxes.append(checkbox)

    def _update_date_range(self, file_date: datetime):
        """Обновляет диапазон дат (минимальная и максимальная даты)."""
        if not self.left_data_for_slider:
            self.left_data_for_slider = file_date
        if not self.right_data_for_slider:
            self.right_data_for_slider = file_date
        self.left_data_for_slider = min(self.left_data_for_slider, file_date)
        self.right_data_for_slider = max(self.right_data_for_slider, file_date)

    def on_done_button_select_logs_view(self):
        if len(self.file_names) == 0:
            self.error.show_error_dialog()
        else:
            dates = [extract_prog_number(file_name)[1] for file_name in self.file_names if extract_prog_number(file_name)[1] != datetime.min]
            if dates:
                self.left_data_for_slider = min(dates)
                self.right_data_for_slider = max(dates)
            else:
                self.left_data_for_slider = datetime.now()
                self.right_data_for_slider = datetime.now()
            self.switch_callback(
                4, file_names=self.file_names,
                left_data_for_slider=self.left_data_for_slider,
                right_data_for_slider=self.right_data_for_slider
            )
            self.frames.date_frame.hide()

    def select_all_up(self):
        """Выделяет или очищает все чекбоксы."""
        all_selected = all(cb["indicatorValue"] for cb in self.checkboxes)
        new_state = 0 if all_selected else 1

        self.file_names.clear()  # Очищаем список перед выбором

        for i, checkbox in enumerate(self.checkboxes):
            checkbox["indicatorValue"] = new_state
            checkbox.setIndicatorValue()
            self._on_checkbox_toggled(new_state, i)
        self.buttons.select_all_up["text"] = "Очистить все" if new_state else "Выбрать все"

    def on_back_button_on_calendar(self):
        self.switch_callback(2)
        self.frames.date_frame.hide()

    def setup(self):
        self.node.hide()

    def show(self, start_date=None, end_date=None):
        """Вызывается при отображении сцены, загружает файлы с нужными датами."""
        super().show()
        self.frames.date_frame.show()

        if start_date and end_date:
            self.start_date = start_date
            self.end_date = end_date
            self.load_file_list(self.start_date, self.end_date)
