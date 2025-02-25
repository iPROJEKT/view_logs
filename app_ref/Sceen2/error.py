from direct.gui.DirectDialog import OkDialog


class ErrorDialogsUI:
    def __init__(self, scene, config, base):
        self.config = config
        self.base = base
        self.scene = scene

        custom_font = self.base.loader.loadFont(self.config.custom_font)

        self.error_date_choice = OkDialog(
            dialogName="ErrorDialog",
            text="Ошибка: конечная дата должна быть позже начальной!",
            buttonTextList=["OK"],
            command=self.close_error_dialog,
            text_font=custom_font,
            text_fg=self.config.text_color,
            relief=None
        )
        self.error_date_choice.hide()

    def show_error_dialog(self):
        """Показать диалог ошибки."""
        self.error_date_choice.show()

    def close_error_dialog(self, _):
        self.error_date_choice.hide()
        self.scene.calendar_app.ui.main_frame.show()
