from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import CardMaker, Texture, NodePath

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Загрузка текстуры с логотипом
        logo_texture = loader.loadTexture("static/img/r_o_y_g_gradient.png")

        # Создание 2D-плоскости для отображения логотипа
        cm = CardMaker("splash")
        cm.setFrame(-1, 1, -1, 1)  # Размер карточки (можно настроить под ваши нужды)

        splash = NodePath(cm.generate())
        splash.setTexture(logo_texture)
        splash.reparentTo(self.render2d)  # Отображение в 2D-слое

        # Установка таймера для скрытия заставки
        self.hideSplashTask = taskMgr.doMethodLater(3, self.hideSplash, "hideSplashTask")

    def hideSplash(self, task):
        # Скрываем заставку
        self.render2d.hide()

        # Здесь можно загрузить и отобразить основное содержимое приложения
        print("Заставка скрыта, загружаем основное приложение...")

        return task.done

app = MyApp()
app.run()