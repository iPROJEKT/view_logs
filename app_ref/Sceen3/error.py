from direct.gui.DirectDialog import OkDialog


class ErrorDialogsUI:
    def __init__(self, config, base, **kwargs):
        self.config = config
        self.base = base
        self.frame = kwargs.get("frame", None)
        self.custom_font = self.base.loader.loadFont(self.config.custom_font)
        self.error_dialog = None  # Будем создавать диалог динамически

    def show_error_dialog(self, message="Ошибка: Вы не выбрали точки для просмотра!"):
        """Показать диалог ошибки с указанным сообщением."""
        # Если диалог уже существует, уничтожаем его
        if self.error_dialog:
            self.error_dialog.destroy()

        self.error_dialog = OkDialog(
            dialogName="ErrorDialog",
            text=message,
            buttonTextList=["OK"],
            command=self.close_error_dialog,
            text_font=self.custom_font,
            text_fg=self.config.text_color,
            relief=None
        )
        self.error_dialog.show()
        if self.frame:
            self.frame.hide()

    def close_error_dialog(self, _):
        """Закрыть диалог ошибки."""
        if self.error_dialog:
            self.error_dialog.hide()
            if self.frame:
                self.frame.show()
