from direct.gui.DirectFrame import DirectFrame


class FramesUI:
    def __init__(self, config):
        self.config = config
        self.start_frame = DirectFrame(
            frameColor=(0, 0, 0, 1),
            frameSize=(-1.9, 1.9, -1.9, 1.9),
        )
