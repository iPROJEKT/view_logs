from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectOptionMenu import DGG

from panda3d.core import TextNode


class InputUI:
    def __init__(self, config, parent, base, **kwargs):
        self.parent = parent
        self.base = base
        self.config = config
        self.kwargs = kwargs

        custom_font = self.base.loader.loadFont(self.config.custom_font)

        self.size_input = DirectEntry(
            scale=0.1,
            pos=(0.25, 0, -0.33),
            parent=self.parent,
            width=3.43,
            initialText="1",
            text_fg=self.config.text_color,
            frameColor=self.config.background_color_choice,
            relief=DGG.FLAT,
            text_align=TextNode.ACenter,
        )
        self.spliter_input = DirectEntry(
            scale=0.1,
            pos=(0.25, 0, -0.17),
            parent=self.parent,
            width=3.43,
            initialText="1",
            text_fg=self.config.text_color,
            frameColor=self.config.background_color_choice,
            relief=DGG.FLAT,
            text_align=TextNode.ACenter,
        )
        self.number_input_top = DirectEntry(
            scale=0.1,
            pos=(1.5, 0, 0.8),
            width=3,
            initialText="100",
            text_fg=self.config.text_color,
            frameColor=self.config.background_color_choice,
            relief=DGG.FLAT,
            text_align=TextNode.ACenter
        )
        self.number_input_bottom = DirectEntry(
            scale=0.1,
            pos=(1.5, 0, -0.85),
            width=3,
            initialText="0",
            text_fg=self.config.text_color,
            frameColor=self.config.background_color_choice,
            relief=DGG.FLAT,
            text_align=TextNode.ACenter
        )
        self.number_input_top.hide()
        self.number_input_bottom.hide()
