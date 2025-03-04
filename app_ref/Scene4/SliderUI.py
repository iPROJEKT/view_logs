from datetime import datetime

from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode
from direct.gui import DirectGuiGlobals as DGG


class SliderUI:
    def __init__(self):
        self.slider = DirectSlider(
            scale=0.65,
            range=(0, 100),
            value=100,
            pos=(0, 0, -0.85),
        )
        self.time_label = DirectLabel(
            text="",
            text_scale=0.05,
            pos=(0, 0, -0.75),  # Позиция над слайдером
            text_align=TextNode.ACenter,
            frameColor=(0, 0, 0, 0.5),
            text_fg=(1, 1, 1, 1),
        )
        self.time_label.hide()
        self.slider.hide()
        thumb = self.slider.thumb
        thumb.bind(DGG.ENTER, self.show_time)
        thumb.bind(DGG.EXIT, self.hide_time)
        self.slider.bind(DGG.ENTER, self.show_time)
        self.slider.bind(DGG.EXIT, self.hide_time)

    def show_time(self, event):
        """Показывает время, соответствующее текущему положению ползунка."""
        if hasattr(self.slider, 'scene_ref'):
            scene = self.slider.scene_ref
            slider_value = self.slider['value']
            time_range = scene.right_time_slider - scene.left_time_slider
            current_time = scene.left_time_slider + (slider_value / 100) * time_range
            current_dt = datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
            self.time_label['text'] = f"{current_dt}"
            self.time_label.show()

    def hide_time(self, event):
        """Скрывает время при уходе курсора."""
        self.time_label.hide()