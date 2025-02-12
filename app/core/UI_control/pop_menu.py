from direct.gui.DirectOptionMenu import DirectOptionMenu, DGG
from panda3d.core import TextNode


class PopMenuUI:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

        custom_font = self.parent.loader.loadFont(self.config.custom_font)

        self.magnitude_menu_filter = DirectOptionMenu(
            text="Фильтрация",
            items=["All", "Into", "Out"],
            text_font=custom_font,
            parent=self.parent.filter_frame,
            pos=(-0.02, 0, 0),
            scale=0.1,
            frameSize=(-1.7, 1.7, -0.65, 0.65),
            text_pos=(0.15, -0.3),
            relief=None,
            popupMarker_relief=None,
            text_align=TextNode.ACenter,
            item_relief=DGG.FLAT,
            item_text_fg=(1, 1, 1, 1),
            item_frameColor=(0.3, 0.3, 0.3, 1),
            text_fg=self.config.text_color
        )
        self.magnitude_menu = DirectOptionMenu(
            text="Величина",
            items=["I", "U", "WFS"],
            parent=self.parent.value_frame,
            command=self.parent.update_labels,
            pos=(-0.02, 0, 0),
            scale=0.1,
            frameSize=(-1.7, 1.7, -0.65, 0.65),
            text_pos=(0.15, -0.3),
            relief=None,
            popupMarker_relief=None,
            text_align=TextNode.ACenter,
            item_relief=DGG.FLAT,
            item_text_fg=(1, 1, 1, 1),
            item_frameColor=(0.3, 0.3, 0.3, 1),
            text_fg=self.config.text_color

        )
