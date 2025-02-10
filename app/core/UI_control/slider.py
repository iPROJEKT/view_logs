from direct.gui.DirectSlider import DirectSlider


class SliderUI:
    def __init__(self, parent):
        self.parent = parent

        self.slider = DirectSlider(
            scale=0.3,
            range=(1, 100),  # Диапазон значений для оси Y
            value=100,  # Начальное значение
            parent=self.parent.info_frame,
            command=self.parent.on_slider_change
        )
