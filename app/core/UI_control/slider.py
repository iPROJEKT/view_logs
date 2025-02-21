from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectOptionMenu import DGG
from panda3d.core import TextNode


class SliderUI:
    def __init__(self, parent):
        self.parent = parent

        self.slider = DirectSlider(
            scale=0.65,
            range=(1, 100),
            value=100,
            pos=(0, 0, -0.85),
            command=self.parent.on_slider_change
        )
        self.slider.hide()
        self.time_label = DirectLabel(
            text="",
            scale=0.05,
            pos=(0, 0, -0.75),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ACenter,
        )
        self.time_label.hide()
        thumb = self.slider.thumb
        thumb.bind(DGG.ENTER, self.parent.show_time_label)
        thumb.bind(DGG.EXIT, self.parent.hide_time_label)
        thumb.bind(DGG.WITHIN, self.parent.update_time_label)
        self.slider.bind(DGG.ENTER, self.parent.show_time_label)
        self.slider.bind(DGG.EXIT, self.parent.hide_time_label)
        self.slider.bind(DGG.WITHIN, self.parent.update_time_label)

