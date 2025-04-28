from datetime import datetime, timedelta

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

            # Преобразуем строки времени из scene в datetime
            try:
                left_dt = datetime.strptime(scene.left_time_slider, '%Y-%m-%d %H:%M')
                right_dt = datetime.strptime(scene.right_time_slider, '%Y-%m-%d %H:%M')
            except ValueError as e:
                print(f"[DEBUG] ValueError in show_time: {e}")
                self.time_label['text'] = "Invalid Time"
                self.time_label.show()
                return

            time_range = (right_dt - left_dt).total_seconds()
            if time_range <= 0:
                self.time_label['text'] = "Invalid Range"
                self.time_label.show()
                return

            # Вычисляем текущее время на основе положения слайдера
            current_time = left_dt + timedelta(seconds=(slider_value / 100) * time_range)
            current_dt_str = current_time.strftime('%m-%d %H:%M')
            self.time_label['text'] = f"{current_dt_str}"
            self.time_label.show()

    def hide_time(self, event):
        """Скрывает время при уходе курсора."""
        self.time_label.hide()