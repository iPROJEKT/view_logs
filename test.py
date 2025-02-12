from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel, DGG


class TooltipApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        custom_font = self.loader.loadFont('static/fonts/Ubuntu-Regular.ttf')
        self.help_button = DirectButton(
            text="?",
            scale=0.1,
            pos=(0.9, 0, 0.8),
            command=self.show_tooltip,
            text_font=custom_font,
        )
        self.hover_label = DirectLabel(
            text="Это подсказка",
            scale=0.05,
            frameColor=(1, 1, 1, 0.8),
            text_fg=(0, 0, 0, 1),
            pos=(0.9, 0, 0.7),
            text_font=custom_font,
        )
        self.hover_label.hide()
        self.help_button.bind(DGG.ENTER, self.show_hover)
        self.help_button.bind(DGG.EXIT, self.hide_hover)
        self.tooltip_frame = DirectFrame(
            frameColor=(1, 1, 1, 0.8),
            frameSize=(-0.4, 0.4, -0.3, 0.3),
            pos=(0, 0, 0),
            state='normal',
            text_font=custom_font,
        )
        self.tooltip_frame.hide()
        self.tooltip_text = DirectLabel(
            text="Это ваша подсказка!\nДобавьте описание здесь.",
            scale=0.05,
            pos=(0, 0, 0.1),
            parent=self.tooltip_frame,
            text_font=custom_font,
        )
        self.close_button = DirectButton(
            text="X",
            scale=0.05,
            pos=(0.35, 0, 0.25),
            parent=self.tooltip_frame,
            command=self.hide_tooltip,
            text_font=custom_font,
        )

    def show_tooltip(self):
        self.tooltip_frame.show()

    def hide_tooltip(self):
        self.tooltip_frame.hide()

    def show_hover(self, event):
        self.hover_label.show()

    def hide_hover(self, event):
        self.hover_label.hide()


app = TooltipApp()
app.run()