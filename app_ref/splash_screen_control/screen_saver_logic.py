from direct.showbase.ShowBaseGlobal import render2d

from app.core.splash_screen_control.splash_UI import SplashScreenUI


class SplashScreenLogic:
    def __init__(self, base, config, switch_callback):
        self.splash_ui = SplashScreenUI(base, config, self.hide_splash)
        self.switch_callback = switch_callback
        self.setup_splash_screen()

    def setup_splash_screen(self):
        self.hide_all_except_splash()
        if self.splash_ui.splash:
            self.splash_ui.splash.show()

    def hide_all_except_splash(self):
        for node in render2d.getChildren():
            if node != self.splash_ui.splash:
                node.hide()

    def hide_splash(self, task):
        for node in render2d.getChildren():
            node.show()
        if self.splash_ui.splash:
            self.splash_ui.splash.removeNode()
            self.splash_ui.splash = None
            self.switch_callback(2)
        return task.done
