import tkinter as tk
from tkinter import filedialog


from app_ref.Sceen2.ButtonUI import ButtonsUI
from app_ref.Sceen2.FrameUI import FramesUI
from app_ref.SceneABS.SceneABS import Screen
from app_ref.config import ConfigApp


class Scene2(Screen):
    def __init__(self, name, base, switch_callback):
        super().__init__(name, base)
        self.name = name
        self.config_app = ConfigApp()
        self.ui_node = self.node.attachNewNode("UI_Scene2")
        self.frames = FramesUI(self.config_app)
        self.buttons = ButtonsUI(
            self.ui_node, base,
            self.config_app,
            self.on_date_confirmed,
            self.frames.start_frame
        )
        self.switch_callback = switch_callback

    def on_date_confirmed(self):
        # Создаем скрытое окно Tkinter
        root = tk.Tk()
        root.withdraw()

        # Открываем диалог выбора файлов
        file_paths = filedialog.askopenfilenames(
            title="Выберите файлы .dt",
            filetypes=[("DT Files", "*.dt")]
        )

        if file_paths:
            print(file_paths)
            self.frames.start_frame.hide()
            self.switch_callback(3, file_paths=list(file_paths))

    def setup(self):
        self.node.hide()

    def show(self, **kwargs):
        """Показывает сцену"""
        super().show()
        self.frames.start_frame.show()

    def hide(self):
        super().hide()