from direct.gui.DirectOptionMenu import DirectOptionMenu, DGG
from panda3d.core import TextNode


class PopMenuUI:
    def __init__(self, config, filter_frame, value_labels, base, **kwargs):
        self.config = config
        self.filter_frame = filter_frame
        self.value_labels = value_labels
        self.base = base

        self.extra_arg = kwargs

        self.top = kwargs.get("top", None)
        self.bottom = kwargs.get("bottom", None)

        custom_font = self.base.loader.loadFont(self.config.custom_font)

        self.magnitude_menu_filter = DirectOptionMenu(
            text="Фильтрация",
            items=["All", "Into", "Out"],
            text_font=custom_font,
            parent=self.filter_frame,
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
            items=["I", "U", "WFS", 'pres1', 'pres2', 'flow1', 'flow2', 'motor'],
            parent=self.value_labels,
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
            text_fg=self.config.text_color,
            command=self.change_help_text
        )

    def change_help_text(self, selected_item=None):
        if selected_item is None:
            selected_item = self.magnitude_menu.get()
        change = {
            'I': 'I',
            'U': 'U',
            'WFS': 'WFS',
            'pres1': 'Bar',
            'pres2': 'Bar',
            'flow1': 'L/min',
            'flow2': 'L/min',
            'motor': 'I'
        }

        unit = change.get(selected_item, 'Unknown')
        self.top.setText(f"{unit} max")
        self.bottom.setText(f"{unit} min")

