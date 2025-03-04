from app.core.config import ConfigApp
from app_ref.splash_screen_control.screen_saver_logic import SplashScreenLogic
from app_ref.SceneABS.SceneABS import Screen


class Scene1(Screen):
    def __init__(self, name, base, switch_callback):
        super().__init__(name, base)
        self.name = name
        self.config_app = ConfigApp()
        self.splash_logic = SplashScreenLogic(base, self.config_app, switch_callback)

    def setup(self):
        pass
