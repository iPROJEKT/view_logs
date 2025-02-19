from panda3d.core import LineSegs, NodePath, Point3


class CompassControl:
    def __init__(self, base):
        self.base = base

        # Создаем 2D-узел для стрелки компаса
        self.compass_node = NodePath("CompassNode")
        self.compass_node.reparentTo(self.base.aspect2d)

        self.arrow = self.create_arrow()
        self.arrow.reparentTo(self.compass_node)

        # Задаем размер и позицию
        self.compass_node.setScale(0.1)  # Размер стрелки
        self.compass_node.setPos(-1.1, 0, -0.85)

        # Добавляем задачу для обновления
        self.base.taskMgr.add(self.update_compass, "UpdateCompassTask")

    def create_arrow(self):
        lines = LineSegs()
        lines.setThickness(5)  # Толщина линий

        # Ось X (красная)
        lines.setColor(1, 0, 0, 1)  # Красный цвет
        lines.moveTo(Point3(0, 0, 0))  # Начало оси X
        lines.drawTo(Point3(1, 0, 0))  # Конец оси X

        # Ось Y (зеленая)
        lines.setColor(0, 1, 0, 1)  # Зеленый цвет
        lines.moveTo(Point3(0, 0, 0))  # Начало оси Y
        lines.drawTo(Point3(0, 1, 0))  # Конец оси Y

        # Ось Z (синяя)
        lines.setColor(0, 0, 1, 1)  # Синий цвет
        lines.moveTo(Point3(0, 0, 0))  # Начало оси Z
        lines.drawTo(Point3(0, 0, 1))  # Конец оси Z

        return NodePath(lines.create())

    def update_compass(self, task):
        """Обновляет ориентацию компаса, чтобы стрелки указывали на глобальные оси."""
        # Получаем ориентацию камеры
        camera_hpr = self.base.camera.getHpr()

        # Инвертируем ориентацию камеры, чтобы компенсировать её вращение
        self.compass_node.setHpr(-camera_hpr)

        return task.cont

