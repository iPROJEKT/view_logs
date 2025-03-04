from direct.showbase.ShowBaseGlobal import render2d
from panda3d.core import CardMaker, NodePath


class SplashScreenUI:
    def __init__(self, base, config, hide_callback):
        self.base = base
        self.config = config
        self.splash = None
        self.create_splash_screen()
        self.base.taskMgr.doMethodLater(3, hide_callback, "hideSplashTask")

    def create_splash_screen(self):
        logo_texture = self.base.loader.loadTexture(self.config.splash_logo)
        cm = CardMaker("splash")
        cm.setFrame(-1, 1, -1.3, 1.3)
        self.splash = NodePath(cm.generate())
        self.splash.setTexture(logo_texture)
        self.splash.reparentTo(render2d)
