from panda3d.core import WindowProperties, Vec3, Point3, Quat, PerspectiveLens, OrthographicLens, Vec2

from app.core.UI_control.variables import Variables
from app.core.compas.compass import CompassControl
from app.core.lsk.lsk import LSKControl


class CameraControl(LSKControl, CompassControl):
    def __init__(self, base):
        self.base = base
        LSKControl.__init__(self, base)
        CompassControl.__init__(self, base)
        self.mouse_is_pressed = False
        self.left_mouse_is_pressed = False
        self.ignore_first_mouse_movement = False
        self.ignore_first_left_mouse_movement = False
        self.dx = 0
        self.dy = 0
        self.zoom_speed = 10
        self.rotation_speed = 0.1
        self.rotation_speed_for_anchor = 0.1
        self.camera_mode = False
        self.anchor_distance = 100
        self.current_p = 0
        self.current_h = 0
        self.anchor_point = None
        self.is_orthographic = False
        self.lens = PerspectiveLens()
        self.lens.setFov(60)
        base.disableMouse()

        self.set_initial_camera_position()

        self.base.accept('mouse3', self.on_mouse_press)
        self.base.accept('mouse3-up', self.on_mouse_release)
        self.base.accept('mouse1', self.on_left_mouse_press)
        self.base.accept('mouse1-up', self.on_left_mouse_release)
        self.base.accept('wheel_up', self.on_wheel_up)
        self.base.accept('wheel_down', self.on_wheel_down)
        self.base.accept('n', self.toggle_camera_mode)
        self.base.accept('o', self.toggle_projection)
        self.base.taskMgr.add(self.update_camera_task, "UpdateCameraTask")

    def toggle_projection(self):
        """Переключение между перспективной и ортографической проекцией."""
        if self.is_orthographic:
            self.base.cam.node().setLens(self.lens)  # Назначаем новую линзу камере
            self.is_orthographic = False
            print("Переключено на перспективную проекцию.")
        else:
            # Переключаемся на ортографическую проекцию
            lens = OrthographicLens()
            lens.setFilmSize(100, 100)  # Устанавливаем размер области видимости
            self.base.cam.node().setLens(lens)  # Назначаем новую линзу камере
            self.is_orthographic = True
            print("Переключено на ортографическую проекцию.")
        self.update_camera_status_text()

    def update_camera_status_text(self):
        """Обновляет текстовое отображение статуса камеры."""
        if self.camera_mode:
            if self.is_orthographic:
                self.base.alt_cam['text'] = 'Якорная камера с ортографическим режимом'
            else:
                self.base.alt_cam['text'] = 'Якорная камера без ортографического режима'
        else:
            if self.is_orthographic:
                self.base.alt_cam['text'] = 'Свободная камера с ортографическим режимом'
            else:
                self.base.alt_cam['text'] = 'Свободная камера без ортографического режима'
        print(f"[STATUS] {self.base.alt_cam['text']}")

    def toggle_camera_mode(self):
        """Переключение между режимами камеры."""
        self.camera_mode = not self.camera_mode  # Переключаем True/False
        self.update_camera_status_text()

    def ignore_first_move(self):
        if self.ignore_first_mouse_movement:
            self.ignore_first_mouse_movement = False
            self.reset_mouse_position()
            return

        mouse_data = self.base.win.getPointer(0)
        center_x = self.base.win.getProperties().getXSize() // 2
        center_y = self.base.win.getProperties().getYSize() // 2

        self.dx = mouse_data.getX() - center_x
        self.dy = mouse_data.getY() - center_y

        self.dx = max(-100, min(100, self.dx))
        self.dy = max(-100, min(100, self.dy))

        print(f"[DEBUG] Mouse moved: dx={self.dx}, dy={self.dy}")

    def set_initial_camera_position(self):
        """Устанавливаем начальную позицию и ориентацию камеры."""
        print("Setting initial camera position...")
        initial_pos = Vec3(-63.80, -528.95, 140.59)

        self.base.camera.setPos(initial_pos)
        self.base.camera.lookAt(Variables.center)

        print(f"Camera initialized at position: {initial_pos},")

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
        if self.camera_mode == 0:  # Обычный режим камеры
            if self.mouse_is_pressed:
                self.handle_camera_pan()

            if self.left_mouse_is_pressed:
                self.handle_camera_rotation()

        elif self.camera_mode == 1:  # Режим вращения вокруг якорной точки
            if self.left_mouse_is_pressed:
                self.handle_anchor_rotation()

        elif self.camera_mode == 1:  # Режим вращения вокруг якорной точки
            if self.left_mouse_is_pressed:
                self.handle_anchor_rotation()

        return task.cont

    def lerp(self, a, b, t):
        return a + (b - a) * t

    def handle_anchor_rotation(self):
        self.ignore_first_move()
        self.anchor_point = Point3(Variables.center)
        if self.dx != 0 or self.dy != 0:
            delta_h = self.dx * self.rotation_speed_for_anchor
            delta_p = self.dy * self.rotation_speed_for_anchor
            self.current_p = max(-89, min(89, self.current_p + delta_p))
            self.current_h = (self.current_h + delta_h) % 360
            quat_h = Quat()
            quat_h.setFromAxisAngle(self.current_h, Vec3(0, 0, 1))  # Вращение вокруг оси Z
            quat_p = Quat()
            quat_p.setFromAxisAngle(self.current_p, Vec3(1, 0, 0))  # Вращение вокруг оси X
            total_quat = quat_h * quat_p
            distance = (self.base.camera.getPos() - self.anchor_point).length()
            new_camera_pos = total_quat.xform(Vec3(0, distance, 0))
            self.base.camera.setPos(self.anchor_point + new_camera_pos)
            self.base.camera.lookAt(self.anchor_point)
            print(f"[DEBUG] New H: {self.current_h}, New P: {self.current_p}, Camera Pos: {self.base.camera.getPos()}")

        self.reset_mouse_position()

    def handle_camera_pan(self):
        """Перемещение камеры по ПКМ с учётом ориентации."""
        self.ignore_first_move()

        if self.dx != 0 or self.dy != 0:
            print(f"[PAN] Mouse moved: dx={self.dx}, dy={self.dy}")

            right_vector = self.base.camera.getQuat().getRight()
            up_vector = self.base.camera.getQuat().getUp()

            move_right = right_vector * self.dx * 0.1
            move_up = up_vector * (-self.dy) * 0.1

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
        center_x = self.base.win.getProperties().getXSize() // 2
        center_y = self.base.win.getProperties().getYSize() // 2
        self.base.win.movePointer(0, center_x, center_y)

        # Проверяем, успешно ли переместился указатель
        mouse_data = self.base.win.getPointer(0)
        print(
            f"[DEBUG] Mouse reset: Current position ({mouse_data.getX()}, {mouse_data.getY()}), Center ({center_x}, {center_y})"
        )

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
        Зум камеры.
        :param direction: 1 для приближения, -1 для отдаления.
        """
        if self.is_orthographic:
            # Если камера в ортографическом режиме
            lens = self.base.cam.node().getLens()
            current_size = lens.getFilmSize()
            new_size = current_size - Vec2(direction * self.zoom_speed, direction * self.zoom_speed)

            # Ограничиваем минимальный и максимальный размер области видимости
            new_size.setX(max(10, min(500, new_size.getX())))
            new_size.setY(max(10, min(500, new_size.getY())))

            lens.setFilmSize(new_size)
            print(f"[ZOOM ORTHO] Film size: {lens.getFilmSize()}")
        else:
            # Если камера в перспективном режиме
            forward_vector = self.base.camera.getQuat().getForward()
            current_pos = self.base.camera.getPos()

            zoom_vector = forward_vector * self.zoom_speed * direction
            new_pos = current_pos + zoom_vector

            self.base.camera.setPos(new_pos)
            print(f"[ZOOM] Camera position: {self.base.camera.getPos()}")

