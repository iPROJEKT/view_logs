from direct.gui.DirectDialog import OkDialog


class ErrorDialogsUI:
    def __init__(self, config, base, **kwargs):
        self.config = config
        self.base = base

        self.extra_arg = kwargs
        self.frame = kwargs.get("frame", None)
        custom_font = self.base.loader.loadFont(self.config.custom_font)

        self.error_empty_logs = OkDialog(
            dialogName="ErrorDialog",
            text="Ошибка: Вы не выбрали точки для просмотра!",
            buttonTextList=["OK"],
            command=self.close_error_dialog,
            text_font=custom_font,
            text_fg=self.config.text_color,
            relief=None
        )
        self.error_empty_logs.hide()

    def show_error_dialog(self):
        """Показать диалог ошибки."""
        self.error_empty_logs.show()
        self.frame.hide()

    def close_error_dialog(self, _):
        self.error_empty_logs.hide()
        self.frame.show()
