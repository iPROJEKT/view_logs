from direct.gui.DirectSlider import DirectSlider


class SliderUI:
    def __init__(self, parent):
        self.parent = parent

        self.slider = DirectSlider(
            scale=0.65,
            range=(1, 100),  # Диапазон значений для оси Y
            value=100,  # Начальное значение
            pos=(0, 0, -0.85),
            command=self.parent.on_slider_change
        )
        self.slider.hide()
