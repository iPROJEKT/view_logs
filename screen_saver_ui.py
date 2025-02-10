from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import CardMaker, NodePath
import subprocess


class ScreenSaver(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        logo_texture = loader.loadTexture("static/img/trinititech.jpg")
        cm = CardMaker("splash")
        cm.setFrame(-1, 1, -1.3, 1.3)
        splash = NodePath(cm.generate())
        splash.setTexture(logo_texture)
        splash.reparentTo(self.render2d)
        self.hideSplashTask = taskMgr.doMethodLater(3, self.hide_splash, "hideSplashTask")

    def hide_splash(self, task):
        print("Заставка скрыта, запускаем основное приложение...")
        subprocess.Popen(["python", "main.py"])
        self.userExit()
        return task.done


if __name__ == '__main__':
    scr = ScreenSaver()
    scr.run()
