from direct.gui.DirectButton import DirectButton


class ButtonsUI:
    def __init__(self, parent, base, config, frame, **kwargs):
        self.parent = parent
        self.base = base
        self.config = config
        self.frame = frame
        self.extra_arg = kwargs

        self.text = kwargs.get("text", None)
        self.scene = kwargs.get("scene", None)
        self.slider = kwargs.get("slider", None)
        self.ri = kwargs.get("ri", None)
        self.le = kwargs.get("le", None)
        self.update = kwargs.get("update", None)
        self.back = kwargs.get("on_back_button_from_point", None)

        custom_font = self.base.loader.loadFont(self.config.custom_font)

        self.open_left_panel_button = DirectButton(
            text=">",
            scale=0.2,
            pos=(-1.8, 0, 0),
            text_font=custom_font,
            command=self.show_left_panel,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.closed_left_panel_button = DirectButton(
            text="<",
            scale=0.1,
            pos=(0.5, 0, 0.8),
            text_font=custom_font,
            command=self.close_left_panel,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice,
            parent=self.frame,
        )
        self.refresh_button = DirectButton(
            text="Обновить",
            scale=self.config.scale_big,
            pos=(0, 0, -0.9),
            text_font=custom_font,
            parent=self.frame,
            relief=None,
            command=self.update,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.points_button = DirectButton(
            text="Точки",
            scale=0.1,
            pos=(-0.2, 0, 0.1),
            frameColor=(0.6, 0.6, 0.6, 1),
            extraArgs=["points"],
            command=self.set_mode_view,
            text_font=custom_font,
            parent=self.frame,
            relief=None,
            text_fg=self.config.text_color,
        )
        self.lines_button = DirectButton(
            text="Линии",
            scale=0.1,
            pos=(0.2, 0, 0.1),
            frameColor=(0.3, 0.3, 0.3, 1),
            extraArgs=["lines"],
            text_font=custom_font,
            command=self.set_mode_view,
            parent=self.frame,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.back_button_from_point = DirectButton(
            text='Назад',
            text_font=custom_font,
            scale=0.1,
            pos=(-1.6, 0, 0.7),
            command=self.back,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )
        self.back_button_from_point.hide()
        self.open_left_panel_button.hide()

    def show_left_panel(self):
        self.open_left_panel_button.hide()
        self.slider.hide()
        self.back_button_from_point.hide()
        self.frame.show()
        self.le.hide()
        self.ri.hide()
        if self.scene and self.scene.camera_control:
            self.scene.camera_control.compass_node.hide()

    def close_left_panel(self):
        self.frame.hide()
        self.slider.show()
        self.le.show()
        self.back_button_from_point.show()
        self.ri.show()
        self.open_left_panel_button.show()
        if self.scene and self.scene.camera_control:
            self.scene.camera_control.compass_node.show()

    def set_mode_view(self, current_mode):
        if current_mode == "points":
            self.points_button["text_bg"] = (33/255, 33/255, 33/255, 1)
            self.lines_button["text_bg"] = self.config.background_color_choice
            self.text['text'] = 'Режим отображения: Точки'
            self.scene.poit_mode = True  # Обновляем poit_mode в Scene4
        else:
            self.points_button["text_bg"] = self.config.background_color_choice
            self.lines_button["text_bg"] = (33/255, 33/255, 33/255, 1)
            self.text['text'] = 'Режим отображения: Линии'
            self.scene.poit_mode = False  # Обновляем poit_mode в Scene4
