from panda3d.core import WindowProperties, Vec3


class CameraControl:
    def __init__(self, base):
        self.base = base
        self.mouse_is_pressed = False
        self.left_mouse_is_pressed = False
        self.ignore_first_mouse_movement = False
        self.ignore_first_left_mouse_movement = False
        self.dx = 0
        self.dy = 0
        self.zoom_speed = 10
        self.rotation_speed = 0.2
        base.disableMouse()

        self.set_initial_camera_position()

        self.base.accept('mouse3', self.on_mouse_press)
        self.base.accept('mouse3-up', self.on_mouse_release)
        self.base.accept('mouse1', self.on_left_mouse_press)
        self.base.accept('mouse1-up', self.on_left_mouse_release)
        self.base.accept('wheel_up', self.on_wheel_up)
        self.base.accept('wheel_down', self.on_wheel_down)
        self.base.taskMgr.add(self.update_camera_task, "UpdateCameraTask")

    def ignore_first_move(self):
        if self.ignore_first_mouse_movement:
            self.ignore_first_mouse_movement = False
            self.reset_mouse_position()
            return

        mouse_data = self.base.win.getPointer(0)
        self.dx = mouse_data.getX() - self.base.win.getProperties().getXSize() // 2
        self.dy = mouse_data.getY() - self.base.win.getProperties().getYSize() // 2

    def set_initial_camera_position(self):
        """Устанавливаем начальную позицию и ориентацию камеры."""
        print("Setting initial camera position...")
        initial_pos = Vec3(-63.80, -528.95, 140.59)
        initial_hpr = Vec3(-26.77, -20.25, 0.45)

        self.base.camera.setPos(initial_pos)
        self.base.camera.setHpr(initial_hpr)

        print(f"Camera initialized at position: {initial_pos}, rotation: {initial_hpr}")

    def show_cursor(self):
        """Показывает курсор мыши."""
        props = WindowProperties()
        props.setCursorHidden(False)
        self.base.win.requestProperties(props)

    def hide_cursor(self):
        """Скрывает курсор мыши."""
        props = WindowProperties()
        props.setCursorHidden(True)
        self.base.win.requestProperties(props)

    def update_camera_task(self, task):
        if self.mouse_is_pressed:
            self.handle_camera_pan()

        if self.left_mouse_is_pressed:
            self.handle_camera_rotation()

        return task.cont

    def handle_camera_pan(self):
        """Перемещение камеры по ПКМ с учётом ориентации."""
        self.ignore_first_move()

        if self.dx != 0 or self.dy != 0:
            print(f"[PAN] Mouse moved: dx={self.dx}, dy={self.dy}")

            right_vector = self.base.camera.getQuat().getRight()
            up_vector = self.base.camera.getQuat().getUp()

            move_right = right_vector * self.dx * 0.1
            move_up = up_vector * self.dy * 0.1

            new_pos = self.base.camera.getPos() + move_right + move_up

            self.base.camera.setPos(new_pos)
            print(f"[PAN] Camera position: {self.base.camera.getPos()}")

        self.reset_mouse_position()

    def handle_camera_rotation(self):
        """Вращение камеры по ЛКМ."""
        self.ignore_first_move()

        if self.dx != 0 or self.dy != 0:
            print(f"[ROTATE] Mouse moved: dx={self.dx}, dy={self.dy}")

            current_hpr = self.base.camera.getHpr()
            new_h = current_hpr.getX() - self.dx * self.rotation_speed
            new_p = current_hpr.getY() - self.dy * self.rotation_speed

            new_p = max(-90, min(90, new_p))

            self.base.camera.setHpr(new_h, new_p, current_hpr.getZ())
            print(f"[ROTATE] Camera rotation: {self.base.camera.getHpr()}")

        self.reset_mouse_position()

    def reset_mouse_position(self):
        """Перемещает указатель мыши в центр экрана."""
        center_x = self.base.win.getProperties().getXSize() // 2
        center_y = self.base.win.getProperties().getYSize() // 2
        self.base.win.movePointer(0, center_x, center_y)

    def on_mouse_press(self):
        self.ignore_first_mouse_movement = False
        self.ignore_first_left_mouse_movement = False
        self.mouse_is_pressed = True
        self.hide_cursor()
        self.reset_mouse_position()
        print("[PRESS] Mouse button pressed (Right)")

    def on_mouse_release(self):
        self.mouse_is_pressed = False
        self.show_cursor()
        self.reset_mouse_position()
        print("[RELEASE] Mouse button released (Right)")

    def on_left_mouse_press(self):
        self.ignore_first_mouse_movement = False
        self.ignore_first_left_mouse_movement = False
        self.left_mouse_is_pressed = True
        self.reset_mouse_position()
        self.hide_cursor()
        print("[PRESS] Mouse button pressed (Left)")

    def on_left_mouse_release(self):
        self.left_mouse_is_pressed = False
        self.show_cursor()
        print("[RELEASE] Mouse button released (Left)")

    def on_wheel_up(self):
        """Обработчик прокрутки колесика вверх."""
        self.zoom_camera(1)

    def on_wheel_down(self):
        """Обработчик прокрутки колесика вниз."""
        self.zoom_camera(-1)

    def zoom_camera(self, direction):
        """
        Зум камеры по направлению её взгляда.
        :param direction: 1 для приближения, -1 для отдаления
        """
        forward_vector = self.base.camera.getQuat().getForward()
        current_pos = self.base.camera.getPos()

        zoom_vector = forward_vector * self.zoom_speed * direction
        new_pos = current_pos + zoom_vector

        self.base.camera.setPos(new_pos)
        print(f"[ZOOM] Camera position: {self.base.camera.getPos()}")
