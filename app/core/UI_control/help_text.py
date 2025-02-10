from direct.gui.DirectLabel import DirectLabel


class TextUI:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

        custom_font = self.parent.loader.loadFont(self.config.custom_font)

        self.filters = DirectLabel(
            text="Filters",
            scale=0.08,
            pos=(-0.1, 0, 0.15),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent.info_frame,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_not_active,
        )
        self.parameters_label = DirectLabel(
            text="Parameters",
            scale=0.08,
            pos=(-0.1, 0, 0.3),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent.info_frame,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_not_active,
        )
