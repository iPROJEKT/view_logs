from direct.gui.DirectEntry import DirectEntry
from panda3d.core import TextNode
from direct.gui.DirectOptionMenu import DGG


class InputFieldsUI:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

        self.number_input_top = DirectEntry(
            scale=0.1,  # Размер поля ввода
            pos=(1.1, 0, 0.8),  # Позиция над изображением
            width=3,  # Ширина поля ввода
            initialText="100",  # Изначальный текст (например, "0")
            text_fg=self.config.text_color,
            frameColor=self.config.background_color_choice,
            relief=DGG.FLAT,
            text_align=TextNode.ACenter
        )
        self.number_input_bottom = DirectEntry(
            scale=0.1,
            pos=(1.1, 0, -0.85),
            width=3,
            initialText="0",
            text_fg=self.config.text_color,
            frameColor=self.config.background_color_choice,
            relief=DGG.FLAT,
            text_align=TextNode.ACenter
        )
        self.number_input_top.hide()
        self.number_input_bottom.hide()

