from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode


class TextUI:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

        custom_font = self.parent.loader.loadFont(self.config.custom_font)

        self.filters = DirectLabel(
            text="Фильтр",
            scale=0.08,
            pos=(-0.15, 0, -0.48),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent.left_user_frame,
            relief=None,
            text_fg=self.config.text_color,
        )
        self.parameters_label = DirectLabel(
            text="Параметр",
            scale=0.08,
            pos=(-0.156, 0, -0.65),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent.left_user_frame,
            relief=None,
            text_fg=self.config.text_color,
        )
        self.size_label = DirectLabel(
            text="Размер",
            scale=0.08,
            pos=(-0.15, 0, -0.32),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent.left_user_frame,
            relief=None,
            text_fg=self.config.text_color,
        )
        self.del_label = DirectLabel(
            text="Делитель",
            scale=0.08,
            pos=(-0.15, 0, -0.17),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent.left_user_frame,
            relief=None,
            text_fg=self.config.text_color,
        )
        self.wamm_label = DirectLabel(
            text="W | A | A | M | M | E | R",
            scale=0.08,
            pos=(0, 0, 0.8),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent.left_user_frame,
            relief=None,
            text_fg=self.config.text_color,
        )
        self.parameters_up_help = DirectLabel(
            text="I max",
            scale=0.08,
            pos=(0.8, 0, 0.8),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_not_active,
        )
        self.parameters_down_help = DirectLabel(
            text="I min",
            scale=0.08,
            pos=(0.8, 0, -0.85),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_not_active,
        )
        self.alt_cam = DirectLabel(
            text='Свободная камера без ортографии',
            scale=0.05,
            pos=(0, 0, 0.7),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_not_active,
        )
        self.hover_label = DirectLabel(
            text=self.config.hover_for_pep_8(),
            scale=0.07,
            frameColor=(1, 1, 1, 0.8),
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_not_active,
            pos=(0, 0, 0.1),
            text_font=custom_font,
        )
        self.alt_cam.hide()
        self.parameters_up_help.hide()
        self.parameters_down_help.hide()
        self.hover_label.hide()
