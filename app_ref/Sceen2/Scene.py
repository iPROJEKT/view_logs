from app_ref.calendar_control.calendar_app import CalendarApp
from app.core.config import ConfigApp
from app_ref.Sceen2.ButtonUI import ButtonsUI
from app_ref.Sceen2.FrameUI import FramesUI
from app_ref.Sceen2.error import ErrorDialogsUI
from app_ref.Sceen2.utils import on_date_selected
from app_ref.SceneABS.SceneABS import Screen


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
        self.calendar_app = CalendarApp(
            self.ui_node,
            self.config_app
        )
        self.error = ErrorDialogsUI(
            self.calendar_app,
            self.config_app,
            base
        )
        self.switch_callback = switch_callback

    def on_date_confirmed(self):
        start_date = str(self.calendar_app.logic.start_date)
        end_date = str(self.calendar_app.logic.end_date)

        if on_date_selected(start_date, end_date) == 1:
            self.error.show_error_dialog()
            self.calendar_app.ui.main_frame.hide()
        else:
            self.calendar_app.ui.main_frame.hide()
            self.frames.start_frame.hide()
            self.switch_callback(3, start_date=start_date, end_date=end_date)

    def setup(self):
        self.node.hide()

    def show(self, **kwargs):
        """Показывает сцену"""
        super().show()
        self.calendar_app.ui.main_frame.show()
        self.frames.start_frame.show()

    def hide(self):
        super().hide()