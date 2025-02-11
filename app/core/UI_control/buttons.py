from direct.gui.DirectButton import DirectButton


class ButtonsUI:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

        custom_font = self.parent.loader.loadFont(self.config.custom_font)

        self.confirm_button = DirectButton(
            text="Выбрать",
            scale=0.1,
            pos=(1, 0, -0.1),
            command=self.parent.on_date_confirmed,
            text_font=custom_font,
            parent=self.parent.start_frame,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.back_button = DirectButton(
            text="Назад",
            scale=0.1,
            pos=(-1, 0, 0.7),
            command=self.parent.on_back_button_pressed,
            text_font=custom_font,
            parent=self.parent.date_frame,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.done_button = DirectButton(
            text="Готово",
            scale=0.1,
            pos=(1, 0, -0.7),
            command=self.parent.on_done_button_pressed,
            text_font=custom_font,
            parent=self.parent.date_frame,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.refresh_button = DirectButton(
            text="Обновить",
            scale=0.08,
            pos=(0.44, 0, -0.03),
            command=self.parent.refresh_gradient,
            text_font=custom_font,
            parent=self.parent.info_frame,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.back_button_from_point_view = DirectButton(
            text="Назад",
            scale=0.1,
            pos=(-1, 0, 0.7),
            text_font=custom_font,
            command=self.parent.back_from_point_view,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.select_all_up = DirectButton(
            scale=0.09,
            text='Выбрать все',
            text_font=custom_font,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice,
            parent=self.parent.date_frame,
            pos=(0.9, 0, 0.7),
            command=self.parent.select_all_up
        )
        self.back_button_from_point_view.hide()
