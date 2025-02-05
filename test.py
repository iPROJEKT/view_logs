from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DGG

class ReliefDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.button_labels = [
            "FLAT", "RAISED", "SUNKEN", "RIDGE",
            "GROOVE", "FRAME", "NONE"
        ]

        self.relief_types = [
            DGG.FLAT, DGG.RAISED, DGG.SUNKEN, DGG.RIDGE,
            DGG.GROOVE,  None
        ]

        self.buttons = []

        for i, (label, relief) in enumerate(zip(self.button_labels, self.relief_types)):
            button = DirectButton(
                text=label,
                scale=0.1,
                pos=(-0.5 + (i % 4) * 0.4, 0, 0.3 - (i // 4) * 0.3),
                relief=relief,
                frameColor=(0.2, 0.2, 0.8, 1),
                text_fg=(1, 1, 1, 1),
            )
            self.buttons.append(button)

app = ReliefDemo()
app.run()