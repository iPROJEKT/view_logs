from direct.showbase.ShowBase import ShowBase

from app_ref.Sceen1.Scene import Scene1 as FirstScene
from app_ref.Sceen2.Scene import Scene2 as SecondScene
from app_ref.Sceen3.Scene import Scene3 as ThirdScene
from app_ref.Scene4.Scene import Scene4 as FourthScene


class ScreenManager(ShowBase):
    def __init__(self):
        super().__init__()
        self.screens = {}
        self.current_screen = None

        self.add_screens([
            (1, FirstScene("Scene1", self, self.switch_screen)),
            (2, SecondScene("Scene2", self, self.switch_screen)),
            (3, ThirdScene("Scene3", self, self.switch_screen)),
            (4, FourthScene("Scene4", self, self.switch_screen)),
        ])
        for screen in self.screens.values():
            screen.setup()
        self.switch_screen(1)

    def add_screens(self, screens):
        """Добавляет список экранов с номерами"""
        for number, screen in screens:
            self.screens[number] = screen

    def switch_screen(self, screen_number, **kwargs):
        """Переключает сцену"""
        if self.current_screen:
            self.current_screen.hide()

        self.current_screen = self.screens.get(screen_number)

        if self.current_screen:
            self.current_screen.show(**kwargs)

