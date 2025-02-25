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
            pos=self.config.pos_optional_menu,
            scale=self.config.scale_big,
            frameSize=self.config.frame_size_optional_menu,
            text_pos=self.config.text_pos,
            relief=None,
            popupMarker_relief=None,
            text_align=TextNode.ACenter,
            item_relief=DGG.FLAT,
            item_text_fg=self.config.item_text_color_white,
            item_frameColor=self.config.item_frame_color_black,
            text_fg=self.config.text_color
        )
        self.magnitude_menu = DirectOptionMenu(
            text="Величина",
            items=["I", "U", "WFS"],
            parent=self.parent.value_frame,
            command=self.parent.update_labels,
            pos=self.config.pos_optional_menu,
            scale=self.config.scale_big,
            frameSize=self.config.frame_size_optional_menu,
            text_pos=self.config.text_pos,
            relief=None,
            popupMarker_relief=None,
            text_align=TextNode.ACenter,
            item_relief=DGG.FLAT,
            item_text_fg=self.config.item_text_color_white,
            item_frameColor=self.config.item_frame_color_black,
            text_fg=self.config.text_color

        )

    def update_labels(self, selected_item):
        if selected_item == "I":
            self.parent.parameters_up_help["text"] = "I max"
            self.parent.parameters_down_help["text"] = "I min"
        elif selected_item == "U":
            self.parent.parameters_up_help["text"] = "U max"
            self.parent.parameters_down_help["text"] = "U min"
        elif selected_item == "WFS":
            self.parent.parameters_up_help["text"] = "WFS max"
            self.parent.parameters_down_help["text"] = "WFS min"
