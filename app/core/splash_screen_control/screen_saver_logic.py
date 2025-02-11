from direct.showbase.ShowBaseGlobal import render2d

from app.core.splash_screen_control.splash_UI import SplashScreenUI


class SplashScreenLogic:
    def __init__(self, base, config):
        self.splash_ui = SplashScreenUI(base, config)
        self.setup_splash_screen()

    def setup_splash_screen(self):
        """Показываем заставку"""
        self.hide_all_elements_except_splash()
        if self.splash_ui.splash:
            self.splash_ui.splash.show()

    def hide_all_elements_except_splash(self):
        """Скрыть все элементы сцены, кроме заставки"""
        if self.splash_ui.splash:
            for node in render2d.getChildren():
                if node != self.splash_ui.splash:
                    node.hide()

    @staticmethod
    def show_all_elements():
        """Показать все элементы сцены"""
        for node in render2d.getChildren():
            node.show()

    def hide_splash(self, task):
        """Скрываем и удаляем заставку"""
        self.show_all_elements()
        if self.splash_ui.splash:
            self.splash_ui.splash.removeNode()
            self.splash_ui.splash = None
        return task.done
