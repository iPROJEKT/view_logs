from direct.gui.DirectLabel import DirectLabel


class ImageUI:
    def __init__(self, config):
        self.config = config
        self.image_label = DirectLabel(
            image=self.config.image_gradient_green_yellow_red,
            scale=(0.1, 0, 0.7),
            pos=(1.5, 0, 0),
        )
        self.image_label.hide()