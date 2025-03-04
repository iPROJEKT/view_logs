from direct.gui.DirectDialog import OkDialog
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectScrolledFrame import DirectScrolledFrame


class ErrorDialogsUI:
    def __init__(self, config, base, **kwargs):
        self.config = config
        self.base = base
        self.extra_arg = kwargs

        self.node = kwargs.get("node", None)
        self.button = kwargs.get("button", None)

        custom_font = self.base.loader.loadFont(self.config.custom_font)

        self.error_gradient = OkDialog(
            dialogName="ErrorGradient",
            text="Ошибка: Верхнее значение градиента должно быть больше нижнего!",
            buttonTextList=["OK"],
            text_font=custom_font,
            command=self.close_error_gradient,
            text_fg=self.config.text_color,
            relief=None
        )
        self.error_gradient.setPos(0, 0, 0.4)
        self.error_gradient.hide()

        # Диалог для ошибки размера точек
        self.error_size = OkDialog(
            dialogName="ErrorSize",
            text="Ошибка: Размер точек должен быть больше 0!",
            buttonTextList=["OK"],
            text_font=custom_font,
            command=self.close_error_size,
            text_fg=self.config.text_color,
            relief=None
        )
        self.error_size.setPos(0, 0, 0.4)
        self.error_size.hide()

        # Диалог для ошибки разделителя
        self.error_spliter = OkDialog(
            dialogName="ErrorSpliter",
            text="Ошибка: Значение разделителя должно быть больше 0!",
            buttonTextList=["OK"],
            text_font=custom_font,
            command=self.close_error_spliter,
            text_fg=self.config.text_color,
            relief=None
        )
        self.error_spliter.setPos(0, 0, 0.4)
        self.error_spliter.hide()

    def close_error_gradient(self, _):
        self.error_gradient.hide()
        self.node.show()
        self.button.show()

    def close_error_size(self, _):
        self.error_size.hide()
        self.node.show()
        self.button.show()

    def close_error_spliter(self, _):
        self.error_spliter.hide()
        self.node.show()
        self.button.show()

    def show_gradient_error(self):
        self.error_gradient.show()

    def show_size_error(self):
        self.error_size.show()

    def show_spliter_error(self):
        self.error_spliter.show()

