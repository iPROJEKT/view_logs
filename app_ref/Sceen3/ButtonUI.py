from direct.gui.DirectButton import DirectButton


class ButtonsUI:
    def __init__(self, parent, base, config, frame, **kwargs):
        self.parent = parent
        self.base = base
        self.config = config
        self.frame = frame
        self.extra_arg = kwargs
        self.on_done_button_select_logs_view = kwargs.get("on_done_button_select_logs_view", None)
        self.on_back_button_on_calendar = kwargs.get("on_back_button_on_calendar", None)
        self.select_all_up = kwargs.get("select_all_up", None)

        custom_font = self.base.loader.loadFont(self.config.custom_font)

        self.back_button_on_calendar = DirectButton(
            text="Назад",
            scale=self.config.scale_big,
            pos=(-1, 0, 0.7),
            text_font=custom_font,
            parent=frame,
            relief=None,
            command=self.on_back_button_on_calendar,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.done_button = DirectButton(
            text="Готово",
            scale=self.config.scale_big,
            pos=(1, 0, -0.7),
            command=self.on_done_button_select_logs_view,
            text_font=custom_font,
            parent=frame,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.select_all_up = DirectButton(
            scale=self.config.scale_mini,
            text='Выбрать все',
            text_font=custom_font,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice,
            parent=frame,
            pos=(0.9, 0, 0.7),
            command=self.select_all_up
        )