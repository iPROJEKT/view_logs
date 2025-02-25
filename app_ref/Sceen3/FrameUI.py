from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectScrolledFrame import DirectScrolledFrame


class FramesUI:
    def __init__(self, config):
        self.config = config
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
        self.date_frame.hide()
