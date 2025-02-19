from direct.gui.DirectButton import DirectButton


class ButtonsUI:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config

        custom_font = self.parent.loader.loadFont(self.config.custom_font)

        self.confirm_button = DirectButton(
            text="Выбрать",
            scale=self.config.scale_big,
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
            scale=self.config.scale_big,
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
            scale=self.config.scale_big,
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
            scale=self.config.scale_big,
            pos=(0, 0, -0.9),
            command=self.parent.refresh_gradient,
            text_font=custom_font,
            parent=self.parent.left_user_frame,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.back_button_from_point_view = DirectButton(
            text="Назад",
            scale=self.config.scale_big,
            pos=(-1, 0, 0.7),
            text_font=custom_font,
            command=self.parent.back_from_point_view,
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
            parent=self.parent.date_frame,
            pos=(0.9, 0, 0.7),
            command=self.parent.select_all_up
        )
        self.help_button = DirectButton(
            text="Подсказка",
            scale=self.config.scale_mini,
            text_font=custom_font,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_not_active,
            parent=self.parent.left_user_frame,
            pos=(-0.15, 0, 1.3),
        )
        self.opent_left_panel_button = DirectButton(
            text=">",
            scale=0.2,
            pos=(-1.2, 0, 0),
            text_font=custom_font,
            command=self.parent.show_panet,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.closed_left_panel_button = DirectButton(
            text="<",
            scale=0.1,
            pos=(0.5, 0, 0.8),
            text_font=custom_font,
            command=self.parent.hide_panel,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice,
            parent=self.parent.left_user_frame,
        )
        self.closed_left_panel_button.hide()
        self.opent_left_panel_button.hide()
        self.back_button_from_point_view.hide()
