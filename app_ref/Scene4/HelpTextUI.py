from direct.gui.DirectLabel import DirectLabel
from direct.gui.OnscreenText import OnscreenText


class HelpTextUI:
    def __init__(self, config, parent, base, **kwargs):
        self.parent = parent
        self.base = base
        self.config = config
        self.kwargs = kwargs

        self.ri = kwargs.get("ri", None)
        self.le = kwargs.get("le", None)

        custom_font = self.base.loader.loadFont(self.config.custom_font)

        self.filters = DirectLabel(
            text="Фильтр",
            scale=0.08,
            pos=(-0.15, 0, -0.48),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent,
            relief=None,
            text_fg=self.config.text_color,
        )
        self.parameters_label = DirectLabel(
            text="Параметр",
            scale=0.08,
            pos=(-0.156, 0, -0.63),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent,
            relief=None,
            text_fg=self.config.text_color,
        )
        self.size_label = DirectLabel(
            text="Размер",
            scale=0.08,
            pos=(-0.15, 0, -0.32),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent,
            relief=None,
            text_fg=self.config.text_color,
        )
        self.del_label = DirectLabel(
            text="Делитель",
            scale=0.08,
            pos=(-0.15, 0, -0.17),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent,
            relief=None,
            text_fg=self.config.text_color,
        )
        self.wamm_label = DirectLabel(
            text="W | A | A | M | M | E | R",
            scale=0.08,
            pos=(0, 0, 0.8),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent,
            relief=None,
            text_fg=self.config.text_color,
        )
        self.choice_text = DirectLabel(
            text="Режим отображения: Точки",
            scale=0.06,
            pos=(0, 0, 0.3),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.parent,
            relief=None,
            text_fg=self.config.background_color_not_active,
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
        self.slider_right_time = OnscreenText(
            text=self.ri,
            scale=0.08,
            font=custom_font,
            fg=self.config.text_color,
            pos=(0.6, -0.7)
        )
        self.slider_left_time = OnscreenText(
            text=self.le,
            scale=0.08,
            font=custom_font,
            fg=self.config.text_color,
            pos=(-0.6, -0.7)
        )
        self.help_text_top = OnscreenText(
            text='I max',
            pos=(1.15, 0.8),
            font=custom_font,
            fg=self.config.text_color,
        )
        self.help_text_bottom = OnscreenText(
            text='I min',
            pos=(1.15, -0.85),
            font=custom_font,
            fg=self.config.text_color,
        )
        self.slider_right_time.hide()
        self.slider_left_time.hide()
        self.alt_cam.hide()
        self.help_text_top.hide()
        self.help_text_bottom.hide()
