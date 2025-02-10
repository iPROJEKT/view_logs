from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectScrolledFrame import DirectScrolledFrame


class FramesUI:
    def __init__(self, config):
        self.config = config

        self.start_frame = DirectFrame(
            frameColor=(0, 0, 0, 1),
            frameSize=(-1.9, 1.9, -1.9, 1.9)
        )
        self.calendar_frame = DirectFrame(
            frameColor=(0.2, 0.2, 0.2, 1),
            frameSize=(-1, 1, -1, 1),
            pos=(0, 0, 0),
            parent=self.start_frame
        )
        self.date_frame = DirectFrame(
            frameColor=(1, 1, 1, 1),
            frameSize=(-1, 1, -0.5, 0.5),
            pos=(0, 0, 0)
        )
        self.scroll_frame = DirectScrolledFrame(
            canvasSize=(-0.6, 0.6, -5, 0),
            frameSize=(-0.99, 0.99, -0.49, 0.49),
            frameColor=(0.2, 0.2, 0.2, 1),
            pos=(0, 0, 0),
            parent=self.date_frame,
            autoHideScrollBars=True,
        )
        self.info_frame = DirectFrame(
            frameColor=self.config.background_color_not_active,
            frameSize=(-0.5, 0.7, -0.1, 0.4),
            pos=(-0.8, 0, -0.8),
        )
        self.filter_frame = DirectFrame(
            frameColor=self.config.background_color_choice,
            frameSize=(-0.18, 0.18, -0.06, 0.06),
            pos=(0.4, 0, 0.18),
            parent=self.info_frame
        )
        self.value_frame = DirectFrame(
            frameColor=self.config.background_color_choice,
            frameSize=(-0.18, 0.18, -0.06, 0.06),
            pos=(0.4, 0, 0.31),
            parent=self.info_frame
        )
        self.calendar_frame.hide()
        self.scroll_frame.hide()
        self.info_frame.hide()
        self.date_frame.hide()
