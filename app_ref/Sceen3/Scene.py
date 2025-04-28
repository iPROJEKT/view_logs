import os
from datetime import datetime

from direct.gui.DirectCheckButton import DirectCheckButton
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode

from app_ref.config import ConfigApp
from app_ref.Sceen3.error import ErrorDialogsUI
from app_ref.Sceen3.ButtonUI import ButtonsUI
from app_ref.Sceen3.FrameUI import FramesUI
from app_ref.Sceen3.utils import extract_prog_number, filter_by_date
from app_ref.SceneABS.SceneABS import Screen
from app_ref.core.tools.const import LOGS_DIR


class Scene3(Screen):
    def __init__(self, name, base, switch_callback):
        super().__init__(name, base)
        self.name = name
        self.config_app = ConfigApp()
        self.node = self.base.aspect2d.attachNewNode("Scene3")
        self.ui_node = self.node.attachNewNode("UI_Scene3")
        self.frames = FramesUI(self.config_app)

        self.buttons = ButtonsUI(
            parent=self.ui_node,
            base=base,
            config=self.config_app,
            frame=self.frames.date_frame,
            on_done_button_select_logs_view=self._on_accept_clicked,
            on_back_button_on_calendar=self._on_back_button_clicked,
            select_all_up=self._on_select_all_clicked,
        )

        self.error = ErrorDialogsUI(
            self.config_app,
            base,
            frame=self.frames.date_frame
        )

        self.switch_callback = switch_callback

        # Списки для файлов
        self.initial_file_pool = []  # Храним пул всех файлов
        self.file_paths = []  # Храним полные пути текущих файлов
        self.file_names = []  # Храним имена файлов для отображения
        self.labels = []
        self.checkboxes = []
        self.left_data_for_slider = None
        self.right_data_for_slider = None
        self.start_date = None
        self.end_date = None
        self.selected_files = []  # Храним выбранные файлы

    def setup(self):
        self.node.hide()

    def show(self, file_paths=None, start_date=None, end_date=None, file_names=None):
        """Display the scene with provided or previously selected files."""
        super().show()
        self.frames.date_frame.show()

        self.start_date = start_date
        self.end_date = end_date

        # Если переданы file_paths или file_names, обновляем пул
        if file_paths or file_names:
            files_to_load = file_names if file_names is not None else file_paths
            self.initial_file_pool = files_to_load  # Сохраняем пул файлов
            self.load_file_list_from_paths(files_to_load)
            if file_names:
                self.selected_files = file_names
                self._restore_checkboxes()
        # Если пул уже существует, загружаем его
        elif self.initial_file_pool:
            self.load_file_list_from_paths(self.initial_file_pool)
            self._restore_checkboxes()
        # Иначе загружаем файлы по датам
        else:
            self.load_file_list(start_date, end_date)

    def _restore_checkboxes(self):
        """Restore checkbox states based on selected_files."""
        for checkbox, file_path in zip(self.checkboxes, self.file_paths):
            checkbox['indicatorValue'] = 1 if file_path in self.selected_files else 0
            checkbox.setIndicatorValue()

    def hide(self):
        super().hide()

    def _on_accept_clicked(self):
        """Handle the 'Accept' button click."""
        selected_files = [
            file_path
            for file_path, checkbox in zip(self.file_paths, self.checkboxes)
            if checkbox['indicatorValue']
        ]

        if not selected_files:
            self.error.show_error_dialog("Ошибка: не выбраны файлы для отображения")
            return

        valid_files = []
        missing_files = []
        for file_path in selected_files:
            if os.path.exists(file_path):
                valid_files.append(file_path)
            else:
                missing_files.append(os.path.basename(file_path))

        if missing_files:
            self.error.show_error_dialog(f"Файлы не найдены: {', '.join(missing_files)}")
            if not valid_files:
                return
        self.selected_files = valid_files

        dates = [
            extract_prog_number(os.path.basename(file_path))[1]
            for file_path in valid_files
            if extract_prog_number(os.path.basename(file_path))[1] != datetime.min
        ]
        if dates:
            self.left_data_for_slider = min(dates)
            self.right_data_for_slider = max(dates)
        else:
            self.left_data_for_slider = datetime.now()
            self.right_data_for_slider = datetime.now()

        print("[DEBUG] Switching to Scene4 with files:", self.selected_files)
        print("[DEBUG] Slider dates:", self.left_data_for_slider, self.right_data_for_slider)

        self.switch_callback(
            4,
            file_names=self.selected_files,
            left_data_for_slider=self.left_data_for_slider,
            right_data_for_slider=self.right_data_for_slider
        )
        self.frames.date_frame.hide()

    def _on_checkbox_toggled(self, file_path, status):
        """Handle checkbox toggle."""
        if status and file_path not in self.selected_files:
            self.selected_files.append(file_path)
        elif not status and file_path in self.selected_files:
            self.selected_files.remove(file_path)

    def _on_select_all_clicked(self):
        """Handle 'Select All' or 'Deselect All' button."""
        all_selected = all(cb["indicatorValue"] for cb in self.checkboxes)
        new_state = 0 if all_selected else 1

        for checkbox, file_path in zip(self.checkboxes, self.file_paths):
            checkbox["indicatorValue"] = new_state
            checkbox.setIndicatorValue()
            if new_state and file_path not in self.selected_files:
                self.selected_files.append(file_path)
            elif not new_state and file_path in self.selected_files:
                self.selected_files.remove(file_path)

        self.buttons.select_all_up["text"] = "Очистить все" if new_state else "Выбрать все"

    def _on_back_button_clicked(self):
        """Handle 'Back' button."""
        self.switch_callback(2)
        self.frames.date_frame.hide()

    def load_file_list(self, start_date: str = None, end_date: str = None):
        """Load file list into scroll frame with date filtering."""
        file_paths = [
            os.path.join(LOGS_DIR, f)
            for f in os.listdir(LOGS_DIR)
            if f.lower().endswith('.dt') and filter_by_date(f, start_date, end_date)
        ]
        file_paths.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))
        self.load_file_list_from_paths(file_paths)

    def load_file_list_from_paths(self, file_paths):
        """Load and display selected files."""
        # Clear old elements
        for label in self.labels:
            label.destroy()
        for checkbox in self.checkboxes:
            checkbox.destroy()

        self.labels.clear()
        self.checkboxes.clear()
        self.file_paths.clear()
        self.file_names.clear()
        self.left_data_for_slider = None
        self.right_data_for_slider = None

        element_height = 0.1
        total_height = len(file_paths) * element_height
        self.frames.scroll_frame['canvasSize'] = (-0.9, 0.9, -total_height, 0.1)

        for i, path in enumerate(file_paths):
            file_name = os.path.basename(path)
            self.file_paths.append(path)
            self.file_names.append(file_name)

            # Extract date
            _, file_date = extract_prog_number(file_name)
            if file_date != datetime.min:
                self._update_date_range(file_date)

            y_pos = -0.03 - i * element_height
            y_pos_check = -0.01 - i * element_height

            # Label text
            label_text = file_name
            if file_date != datetime.min:
                label_text += f" ({file_date.strftime('%d-%m-%Y %H:%M:%S')})"

            # Label
            label = DirectLabel(
                text=label_text,
                text_align=TextNode.ALeft,
                scale=0.07,
                pos=(-0.75, 0, y_pos),
                parent=self.frames.scroll_frame.getCanvas(),
                frameColor=(0, 0, 0, 0),
            )
            self.labels.append(label)

            # Checkbox
            checkbox = DirectCheckButton(
                scale=0.05,
                pos=(0.8, 0, y_pos_check),
                parent=self.frames.scroll_frame.getCanvas(),
                indicatorValue=1 if path in self.selected_files else 0,
                command=self._on_checkbox_toggled,
                extraArgs=[path],  # Pass file_path instead of index
                relief=None,
            )
            self.checkboxes.append(checkbox)

    def _update_date_range(self, file_date: datetime):
        """Update the date range (min and max dates)."""
        if not self.left_data_for_slider:
            self.left_data_for_slider = file_date
        if not self.right_data_for_slider:
            self.right_data_for_slider = file_date
        self.left_data_for_slider = min(self.left_data_for_slider, file_date)
        self.right_data_for_slider = max(self.right_data_for_slider, file_date)