from direct.gui.DirectOptionMenu import DirectOptionMenu, DGG
from panda3d.core import TextNode


class PopMenuUI:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

        custom_font = self.parent.loader.loadFont(self.config.custom_font)

        self.magnitude_menu_filter = DirectOptionMenu(
            text="Фильтрация",
            text_scale=0.1,
            item_text_scale=0.1,
            highlightScale=(0.1, 0.1),
            items=["All", "Into", "Out"],
            initialitem=0,
            frameSize=(-0.18, 0.18, -0.06, 0.06),
            pos=(0, 0, -0.03),
            text_font=custom_font,
            parent=self.parent.filter_frame,
            popupMarker_relief=None,
            relief=None,
            item_frameColor=(0.3, 0.3, 0.3, 1),
            item_text_fg=(1, 1, 1, 1),
            item_relief=DGG.FLAT,
            text_fg=self.config.text_color,
            text_align=TextNode.ACenter,
            item_frameTexture=None,
            item_image=None
        )
        self.magnitude_menu = DirectOptionMenu(
            text="Величина",
            text_scale=0.1,
            item_text_scale=0.1,
            highlightScale=(0.1, 0.1),
            items=["I", "U", "WFS"],
            initialitem=0,
            frameSize=(-0.18, 0.18, -0.06, 0.06),
            pos=(0, 0, -0.03),
            text_font=custom_font,
            parent=self.parent.value_frame,
            popupMarker_relief=None,
            relief=None,
            item_frameColor=(0.3, 0.3, 0.3, 1),
            item_text_fg=(1, 1, 1, 1),
            item_relief=DGG.FLAT,
            text_fg=self.config.text_color,
            text_align=TextNode.ACenter,
            item_frameTexture=None,
            item_image=None,
            command=self.parent.update_labels
        )
