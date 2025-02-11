from direct.gui.DirectDialog import OkDialog


class ErrorDialogsUI:
    def __init__(self, parent, config):
        self.config = config
        self.parent = parent

        custom_font = self.parent.loader.loadFont(self.config.custom_font)

        # Инициализация диалогов
        self.error_dialog = OkDialog(
            dialogName="ErrorDialog",
            text="Ошибка: конечная дата должна быть позже начальной!",
            buttonTextList=["OK"],
            command=self.close_error_dialog,
            text_font=custom_font,
            text_fg=self.config.text_color,
            relief=None
        )
        self.error_min_max = OkDialog(
            dialogName="ErrorMinMax",
            text="Ошибка: Максимальное значение не может быть меньше или равно минимальному!",
            buttonTextList=["OK"],
            command=self.close_error_min_max,
            text_font=custom_font,
            text_fg=self.config.text_color,
            relief=None,
            text_bg=self.config.background_color_choice
        )

        self.error_empty_log = OkDialog(
            dialogName="ErrorEmptyLog",
            text="Ошибка: Вы не выбрали логи!",
            buttonTextList=["OK"],
            command=self.close_error_empty_log,
            text_font=custom_font,
            text_fg=self.config.text_color,
            relief=None,
        )

        # Инициализация всех диалогов как скрытых
        self.error_dialog.hide()
        self.error_min_max.hide()
        self.error_empty_log.hide()
