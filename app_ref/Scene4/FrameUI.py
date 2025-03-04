from direct.gui.DirectFrame import DirectFrame


class FramesUI:
    def __init__(self, config):
        self.config = config
        self.left_user_frame = DirectFrame(
            frameColor=(33 / 255, 33 / 255, 33 / 255, 1),
            frameSize=(-0.45, 0.45, -1, 1),
            pos=(-1.44, 0, 0),
        )
        self.filter_frame = DirectFrame(
            frameColor=self.config.background_color_choice,
            frameSize=(-0.18, 0.18, -0.07, 0.07),
            pos=(0.25, 0, -0.605),
            parent=self.left_user_frame
        )
        self.value_frame = DirectFrame(
            frameColor=self.config.background_color_choice,
            frameSize=(-0.18, 0.18, -0.07, 0.07),
            pos=(0.25, 0, -0.45),
            parent=self.left_user_frame
        )
        self.left_user_frame.hide()

    def hide(self):
        self.left_user_frame.hide()
