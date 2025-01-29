from direct.gui.DirectButton import DirectButton
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectOptionMenu import DirectOptionMenu
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.DirectSlider import DirectSlider


class MyAppInit:
    def __init__(self):
        self.point_cloud_nodes = []
        self.checkboxes = []
        self.labels = []
        self.file_names = []
        self.point_cloud_data = {}
        self.num_layers = 10
        self.setBackgroundColor(0, 0, 0)
        self.saved_gradient_param = None
        self.saved_filter_type = None
        self.saved_min = None
        self.saved_max = None

        image_gradient_green_yellow_red = loader.loadTexture('static/img/r_o_y_g_gradient.png')
        custom_font = loader.loadFont('static/fonts/Ubuntu-Regular.ttf')
        self.slider_timer = None
        self.start_frame = DirectFrame(
            frameColor=(0, 0, 0, 1),
            frameSize=(-1.9, 1.9, -1.9, 1.9)
        )
        self.year_menu_first, self.month_menu_first, self.day_menu_first = self.create_date_selectors(
            y_offset=0,
            font=custom_font,
        )
        self.year_menu_second, self.month_menu_second, self.day_menu_second = self.create_date_selectors(
            y_offset=-0.3,
            font=custom_font,
        )
        self.confirm_button = DirectButton(
            text="Выбрать",
            scale=0.1,
            pos=(1, 0, -0.1),
            command=self.on_date_confirmed,
            text_font=custom_font,
            parent=self.start_frame,
        )
        self.date_frame = DirectFrame(
            frameColor=(1, 1, 1, 1),
            frameSize=(-1, 1, -0.5, 0.5),
            pos=(0, 0, 0)
        )
        self.back_button = DirectButton(
            text="Назад",
            scale=0.1,
            pos=(-1, 0, 0.7),
            command=self.on_back_button_pressed,
            text_font=custom_font,
            parent=self.date_frame,
        )
        self.done_button = DirectButton(
            text="Готово",
            scale=0.1,
            pos=(1, 0, -0.7),
            command=self.on_done_button_pressed,
            text_font=custom_font,
            parent=self.date_frame,
        )
        self.scroll_frame = DirectScrolledFrame(
            canvasSize=(-0.6, 0.6, -5, 0),
            frameSize=(-0.99, 0.99, -0.49, 0.49),
            frameColor=(0.2, 0.2, 0.2, 1),
            pos=(0, 0, 0),
            parent=self.date_frame,
        )
        self.image_label = DirectLabel(
            image=image_gradient_green_yellow_red,  # Устанавливаем текстуру
            scale=(0.1, 0, 0.7),  # Масштабируем изображение
            pos=(1.1, 0, 0),  # Позиция на экране
        )
        self.number_input_top = DirectEntry(
            scale=0.1,  # Размер поля ввода
            pos=(1, 0, 0.8),  # Позиция над изображением
            width=3,  # Ширина поля ввода
            initialText="100",  # Изначальный текст (например, "0")
            focus=True,  # Фокус на поле при старте
        )
        self.number_input_bottom = DirectEntry(
            scale=0.1,  # Размер поля ввода
            pos=(1, 0, -0.85),  # Позиция под изображением
            width=3,  # Ширина поля ввода
            initialText="0",  # Изначальный текст (например, "0")
            focus=True,  # Фокус на поле при старте # Команда при изменении текста
        )
        self.info_frame = DirectFrame(
            frameColor=(0.1, 0.1, 0.1, 0.8),  # полупрозрачный фон
            frameSize=(-0.5, 0.7, -0.1, 0.4),  # размер окна
            pos=(-0.8, 0, -0.8),  # позиция внизу слева
        )
        self.filters = DirectLabel(
            text="Filters",  # Текст
            scale=0.08,  # Размер шрифта
            pos=(-0.1, 0, 0.19),  # Координаты: немного левее от magnitude_menu
            text_font=custom_font,  # Используем тот же шрифт
            frameColor=(0, 0, 0, 0),  # Прозрачный фон
            parent=self.info_frame  # Привязываем к info_frame
        )
        self.parameters_label = DirectLabel(
            text="Parameters",  # Текст
            scale=0.08,  # Размер шрифта
            pos=(-0.1, 0, 0.3),  # Координаты: немного левее от magnitude_menu
            text_font=custom_font,  # Используем тот же шрифт
            frameColor=(0, 0, 0, 0),  # Прозрачный фон
            parent=self.info_frame  # Привязываем к info_frame
        )
        self.magnitude_menu_filter = DirectOptionMenu(
            text="Фильтрация", scale=0.1, items=["All", "Into", "Out"], initialitem=0,
            pos=(0.4, 0, 0.19), text_font=custom_font, parent=self.info_frame
        )
        self.magnitude_menu = DirectOptionMenu(
            text="Величина", scale=0.1, items=["I", "U", "WFS"], initialitem=0,
            pos=(0.4, 0, 0.3), text_font=custom_font, parent=self.info_frame
        )
        self.refresh_button = DirectButton(
            text="Refresh",
            scale=0.08,
            pos=(0.49, 0, -0.03),  # Координаты относительно info_frame
            command=self.refresh_gradient,  # Привязываем метод для обновления
            text_font=custom_font,
            parent=self.info_frame
        )
        self.slider = DirectSlider(
            scale=0.3,
            range=(1, 100),  # Диапазон значений для оси Y
            value=100,  # Начальное значение
            parent=self.info_frame,
            command=self.on_slider_change
        )
        # hide frame
        self.image_label.hide()
        self.scroll_frame.hide()
        self.info_frame.hide()
        self.date_frame.hide()
        self.number_input_top.hide()
        self.number_input_bottom.hide()
