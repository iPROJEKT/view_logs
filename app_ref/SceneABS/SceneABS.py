from direct.showbase.ShowBase import ShowBase
from abc import ABC, abstractmethod

from panda3d.core import NodePath


class Screen(ABC):
    """Базовый класс экрана (сцены)"""
    def __init__(self, name, base: ShowBase):
        self.base = base
        base.setBackgroundColor(0, 0, 0)

        self.node = NodePath(name)
        self.node.reparentTo(base.render)
        self.node.hide()  # По умолчанию скрываем сцену

    @abstractmethod
    def setup(self):
        pass

    def show(self):
        print(f"🔵 Показываем {self.node.getName()}")
        self.node.show()

    def hide(self):
        print(f"⚫ Прячем {self.node.getName()}")
        self.node.hide()

    def destroy(self):
        self.node.removeNode()