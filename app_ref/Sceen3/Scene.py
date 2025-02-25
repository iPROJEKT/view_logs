import os
from datetime import datetime

from direct.gui.DirectCheckButton import DirectCheckButton
from direct.gui.DirectLabel import DirectLabel

from app.core.config import ConfigApp
from app.core.tools.const import LOGS_DIR
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

        self.ui_node = self.node.attachNewNode("UI_Scene3")
        self.frames = FramesUI(self.config_app)

        self.switch_callback = switch_callback

    def _on_checkbox_toggled(self, value, index):
        """Обработчик переключения чекбоксов."""
        file_name = self.labels[index]['text']
        if value and file_name not in self.file_names:
            self.file_names.append(file_name)
        elif not value and file_name in self.file_names:
            self.file_names.remove(file_name)
        print(f"Выбранные файлы: {self.file_names}")

    def load_file_list(self, start_date: str = None, end_date: str = None):
        """Загружает список файлов в скроллируемый фрейм с фильтрацией по дате."""
        file_names = [
            f for f in os.listdir(LOGS_DIR)
            if f.endswith('.dt') and filter_by_date(f, start_date, end_date)
        ]
        file_names.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

        # Обновляем размеры скролла
        element_height = 0.1
        total_height = len(file_names) * element_height
        self.frames.scroll_frame['canvasSize'] = (-0.9, 0.9, -total_height, 0.1)

        # Отрисовка элементов
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
            text=file_name, scale=0.07, pos=(-0.3, 0, y_pos),
            parent=self.frames.scroll_frame.getCanvas(), frameColor=(0, 0, 0, 0),
        )
        self.labels.append(label)

        checkbox = DirectCheckButton(
            scale=0.05, pos=(0.8, 0, y_pos_check), parent=self.frames.scroll_frame.getCanvas(),
            indicatorValue=0, command=self._on_checkbox_toggled, extraArgs=[index],
            relief=None,
        )
        self.checkboxes.append(checkbox)

    def _update_date_range(self, file_date: datetime):
        """Обновляет диапазон дат (минимальная и максимальная даты)."""
        self.last_data = min(self.last_data, file_date) if self.last_data else file_date
        self.end_data = max(self.end_data, file_date) if self.end_data else file_date

    def setup(self):
        self.node.hide()

    def show(self):
        super().show()
        self.frames.date_frame.show()
