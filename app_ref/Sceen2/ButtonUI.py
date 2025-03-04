import webbrowser

from direct.gui.DirectButton import DirectButton


class ButtonsUI:
    def __init__(self, parent, base, config, on_date_confirmed, frame):
        self.parent = parent
        self.base = base
        self.config = config
        self.on_date_confirmed = on_date_confirmed
        self.frame = frame

        custom_font = self.base.loader.loadFont(self.config.custom_font)

        self.confirm_button = DirectButton(
            text="Выбрать",
            scale=self.config.scale_big,
            pos=(1.3, 0, -0.1),
            command=self.on_date_confirmed,
            text_font=custom_font,
            parent=self.frame,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )

        def open_feedback_form():
            webbrowser.open("https://forms.gle/dGE6HrTxRVqx3Rv87")

        self.relate_name = DirectButton(
            text='Обратная связь',
            scale=self.config.scale_big,
            pos=(1.4, 0, -0.8),
            command=open_feedback_form,
            text_font=custom_font,
            parent=self.frame,
            relief=None,
            text_fg=self.config.text_color,
            text_bg=self.config.background_color_choice
        )