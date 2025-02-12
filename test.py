from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectOptionMenu, DirectFrame, DGG
from panda3d.core import TextNode


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Создаем фрейм (окно)
        self.info_frame = DirectFrame(
            frameColor=(46 / 255, 46 / 255, 46 / 255, 1),
            frameSize=(-0.5, 0.7, -0.1, 0.4),
            pos=(-0.8, 0, -0.8),
        )
        self.filter_frame = DirectFrame(
            frameColor=(46 / 255, 200 / 255, 46 / 255, 1),
            frameSize=(-0.18, 0.18, -0.06, 0.06),
            pos=(0.4, 0, 0.18),
            parent=self.info_frame
        )
        self.value_frame = DirectFrame(
            frameColor=(46 / 255, 100 / 255, 46 / 255, 1),
            frameSize=(-0.18, 0.18, -0.06, 0.06),
            pos=(0.4, 0, 0.31),
            parent=self.info_frame
        )

        # Создаем DirectOptionMenu
        self.magnitude_menu = DirectOptionMenu(
            text="Величина",
            items=["I", "U", "WFS"],
            pos=(-0.02, 0, 0),
            scale=0.1,
            frameSize=(-1.7, 1.7, -0.65, 0.65),
            text_pos=(0.15, -0.3),
            relief=None,
            popupMarker_relief=None,
            text_align=TextNode.ACenter,
            item_relief=DGG.FLAT,
            item_text_fg=(1, 1, 1, 1),
            item_frameColor=(0.3, 0.3, 0.3, 1),
        )


if __name__ == '__main__':
    app = MyApp()
    app.run()