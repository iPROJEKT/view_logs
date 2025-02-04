from direct.gui.DirectButton import DirectButton
from direct.gui.DirectDialog import OkDialog
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
        self.save_data_h = None
        self.save_data_l = None
        self.slider_timer = None
        self.save_camera_allowed = False



        image_gradient_green_yellow_red = loader.loadTexture('static/img/r_o_y_g_gradient.png')
        custom_font = loader.loadFont('static/fonts/Ubuntu-Regular.ttf')




        self.start_frame = DirectFrame(
            frameColor=(0, 0, 0, 1),
            frameSize=(-1.9, 1.9, -1.9, 1.9)
        )
        self.confirm_button = DirectButton(
            text="Выбрать",
            scale=0.1,
            pos=(1, 0, -0.2),
            command=self.on_date_confirmed,
            text_font=custom_font,
            parent=self.start_frame,
            relief=None,
            text_fg=(1, 1, 1, 1),
            text_bg=(46 / 255, 46 / 255, 46 / 255, 1)
        )
        self.open_calendar_first = DirectButton(
            text="Начальная дата",
            scale=0.15,
            pos=(0, 0, 0.2),
            command=self.calendar_popup,
            parent=self.start_frame,
            text_font=custom_font,
            relief=None,
            text_fg=(1, 1, 1, 1),
            text_bg=(46/255, 46/255, 46/255, 1),
            extraArgs=["first"],
        )
        self.open_calendar_second = DirectButton(
            text="Конечная дата",
            scale=0.15,
            pos=(0, 0, -0.4),
            command=self.calendar_popup,
            parent=self.start_frame,
            text_font=custom_font,
            relief=None,
            text_fg=(1, 1, 1, 1),
            text_bg=(46/255, 46/255, 46/255, 1),
            extraArgs=["second"],
        )
        self.calendar_frame = DirectFrame(
            frameColor=(0.2, 0.2, 0.2, 1),
            frameSize=(-1, 1, -1, 1),
            pos=(0, 0, 0),
            parent=self.start_frame
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

        # Последний фрейм
        self.info_frame = DirectFrame(
            frameColor=(0.1, 0.1, 0.1, 0.8),
            frameSize=(-0.5, 0.7, -0.1, 0.4),
            pos=(-0.8, 0, -0.8),
        )
        self.filters = DirectLabel(
            text="Filters",
            scale=0.08,
            pos=(-0.1, 0, 0.19),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.info_frame
        )
        self.parameters_label = DirectLabel(
            text="Parameters",
            scale=0.08,
            pos=(-0.1, 0, 0.3),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            parent=self.info_frame
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
            pos=(0.49, 0, -0.03),
            command=self.refresh_gradient,
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
        self.back_button_from_point_view = DirectButton(
            text="Назад",
            scale=0.1,
            pos=(-1, 0, 0.7),
            text_font=custom_font,
            command=self.back_from_point_view
        )
        # Обработчик ошибок
        self.error_dialog = OkDialog(
            dialogName="ErrorDialog",
            text="Ошибка: конечная дата должна быть позже начальной!",
            buttonTextList=["OK"],
            command=self.close_error_dialog,
            text_font=custom_font
        )
        self.error_min_max = OkDialog(
            dialogName="ErrorMinMax",
            text="Ошибка: Максимальное значние не может быть меньше или равно минимальному!",
            buttonTextList=["OK"],
            command=self.close_error_min_max,
            text_font=custom_font
        )

        self.back_button_from_point_view.hide()
        self.image_label.hide()
        self.scroll_frame.hide()
        self.info_frame.hide()
        self.date_frame.hide()
        self.number_input_top.hide()
        self.number_input_bottom.hide()
        self.error_dialog.hide()
        self.error_min_max.hide()
        self.calendar_frame.hide()
