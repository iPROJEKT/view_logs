from direct.showbase.ShowBaseGlobal import render2d
from panda3d.core import CardMaker, NodePath


class SplashScreenUI:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.splash = None
        self.create_splash_screen()
        self.hideSplashTask = self.parent.taskMgr.doMethodLater(3, self.parent.hide_splash, "hideSplashTask")

    def create_splash_screen(self):
        """Создаёт заставку"""
        logo_texture = self.parent.loader.loadTexture(self.config.splash_logo)
        cm = CardMaker("splash")
        cm.setFrame(-1, 1, -1.3, 1.3)
        self.splash = NodePath(cm.generate())
        self.splash.setTexture(logo_texture)
        self.splash.reparentTo(render2d)
