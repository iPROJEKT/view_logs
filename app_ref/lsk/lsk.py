from panda3d.core import LineSegs, NodePath, Point3


class LSKControl:
    def __init__(self, base):
        self.base = base

        # Создаем 3D-узел для осей
        self.axes_node = NodePath("AxesNode")
        self.axes_node.reparentTo(self.base.render)

        self.axes = self.create_axes()
        self.axes.reparentTo(self.axes_node)

        # Задаем размер и позицию
        self.axes_node.setScale(1)  # Размер осей
        self.axes_node.setPos(0, 0, 0)  # Позиция осей в мире

    def create_axes(self):
        lines = LineSegs()
        lines.setThickness(5)  # Толщина линий

        # Ось X (красная)
        lines.setColor(1, 0, 0, 1)  # Красный цвет
        lines.moveTo(Point3(0, 0, 0))  # Начало оси X
        lines.drawTo(Point3(40, 0, 0))  # Конец оси X

        # Ось Y (зеленая)
        lines.setColor(0, 1, 0, 1)  # Зеленый цвет
        lines.moveTo(Point3(0, 0, 0))  # Начало оси Y
        lines.drawTo(Point3(0, 40, 0))  # Конец оси Y

        # Ось Z (синяя)
        lines.setColor(0, 0, 1, 1)  # Синий цвет
        lines.moveTo(Point3(0, 0, 0))  # Начало оси Z
        lines.drawTo(Point3(0, 0, 40))  # Конец оси Z

        return NodePath(lines.create())

