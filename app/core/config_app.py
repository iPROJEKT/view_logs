class ConfigApp:
    def __init__(self):
        self.config = {
            'disable-sticky-keys': False,
            'gl-debug': True,
            'gl-debug-errors': True
        }
        self.image_gradient_green_yellow_red = 'static/img/r_o_y_g_gradient.png'
        self.image_for_logo = 'static/img/trinititech.jpg'
        self.custom_font = 'static/fonts/Ubuntu-Regular.ttf'
        self.splash_logo = 'static/img/trinititech.jpg'
        self.text_color = (1, 1, 1, 1)
        self.background_color_choice = (46 / 255, 46 / 255, 46 / 255, 1)
        self.background_color_not_active = (0, 0, 0, 0.8)
        self.pos_optional_menu = (-0.02, 0, 0)
        self.scale_big = 0.1
        self.scale_mini = 0.09
        self.text_pos = (0.15, -0.3)
        self.item_text_color_white = (1, 1, 1, 1)
        self.item_frame_color_black = (0.3, 0.3, 0.3, 1)
        self.frame_size_optional_menu = (-1.7, 1.7, -0.65, 0.65)

    @staticmethod
    def hover_for_pep_8():
        text = 'All - показывает все точки\n'
        text += 'Out - точки за пределами диапазона\n'
        text += 'Into - показывает точки внутри диапазона\n'
        text += 'Задавать диапазон ...max и ...min'
        return text

    def GetBool(self, key, default=False):
        return self.config.get(key, default)
