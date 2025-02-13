from datetime import datetime

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DGG
from panda3d.core import TextNode


class CalendarUI:
    def __init__(self, config):
        self.config = config
        custom_font = loader.loadFont('static/fonts/Ubuntu-Regular.ttf')
        self.frame = DirectFrame(
            frameColor=(0, 0, 0, 1),
            frameSize=(-0.8, 0.8, -0.6, 0.6),
            pos=(0, 0, 0.25),
        )
        self.frame.hide()
        self.start_help_text = DirectLabel(
            text='Выберите диапазон дат для отображения УП',
            scale=0.08,
            pos=(0, 0, 0.7),
            text_font=custom_font,
            frameColor=(0, 0, 0, 0),
            relief=None,
            text_fg=self.config.background_color_choice,
            text_bg=self.config.background_color_not_active,
        )
        self.open_calendar_first = DirectButton(
            text="Начальная дата",
            scale=0.15,
            pos=(0, 0, 0.2),
            command=self.calendar_popup,
            text_font=custom_font,
            relief=None,
            text_fg=(1, 1, 1, 1),
            text_bg=(46 / 255, 46 / 255, 46 / 255, 1),
            extraArgs=["first"],
        )
        self.open_calendar_second = DirectButton(
            text="Конечная дата",
            scale=0.15,
            pos=(0, 0, -0.4),
            command=self.calendar_popup,
            text_font=custom_font,
            relief=None,
            text_fg=(1, 1, 1, 1),
            text_bg=(46 / 255, 46 / 255, 46 / 255, 1),
            extraArgs=["second"],
        )
        self.frame.hide()  # Начинаем с скрытого состояния
        self.month_label = OnscreenText(
            text="", pos=(0, 0.4), scale=0.07, parent=self.frame,
            fg=(1, 1, 1, 1), font=custom_font
        )
        self.year_label = OnscreenText(
            text="", pos=(0, 0.5), scale=0.07, parent=self.frame,
            fg=(1, 1, 1, 1), font=custom_font
        )

        self.prev_month_frame = DirectFrame(
            frameColor=self.config.background_color_choice,
            frameSize=(-0.08, 0.08, -0.04, 0.04),
            pos=(-0.4, 0, 0.42),
            parent=self.frame
        )
        self.prev_month_button = DirectButton(
            text="<", pos=(0, 0, -0.02),
            text_scale=(0.1, 0.1),
            frameSize=(-0.08, 0.08, -0.04, 0.04),
            command=self.change_month, extraArgs=[-1],
            text_align=TextNode.ACenter,
            text_fg=self.config.text_color,
            relief=None,
            parent=self.prev_month_frame,
        )

        # Фрейм для кнопки "Следующий месяц"
        self.next_month_frame = DirectFrame(
            frameColor=self.config.background_color_choice,
            frameSize=(-0.08, 0.08, -0.04, 0.04),
            pos=(0.4, 0, 0.42),
            parent=self.frame
        )
        self.next_month_button = DirectButton(
            text=">", pos=(0, 0, -0.02),
            text_scale=(0.1, 0.1),
            frameSize=(-0.08, 0.08, -0.04, 0.04),
            command=self.change_month, extraArgs=[1],
            text_align=TextNode.ACenter,
            text_fg=self.config.text_color,
            relief=None,
            parent=self.next_month_frame,
        )

        # Фрейм для кнопки "Предыдущий год"
        self.prev_year_frame = DirectFrame(
            frameColor=self.config.background_color_choice,
            frameSize=(-0.08, 0.08, -0.04, 0.04),
            pos=(-0.4, 0, 0.52),
            parent=self.frame
        )
        self.prev_year_button = DirectButton(
            text="<<", pos=(0, 0, -0.02),
            text_scale=(0.1, 0.1),
            frameSize=(-0.08, 0.08, -0.04, 0.04),
            command=self.change_year, extraArgs=[-1],
            text_align=TextNode.ACenter,
            text_fg=self.config.text_color,
            relief=None,
            parent=self.prev_year_frame,
        )

        # Фрейм для кнопки "Следующий год"
        self.next_year_frame = DirectFrame(
            frameColor=self.config.background_color_choice,
            frameSize=(-0.08, 0.08, -0.04, 0.04),
            pos=(0.4, 0, 0.52),
            parent=self.frame
        )
        self.next_year_button = DirectButton(
            text=">>", pos=(0, 0, -0.02),
            text_scale=(0.1, 0.1),
            frameSize=(-0.08, 0.08, -0.04, 0.04),
            command=self.change_year, extraArgs=[1],
            text_align=TextNode.ACenter,
            text_fg=self.config.text_color,
            relief=None,
            parent=self.next_year_frame,
        )

        self.day_buttons = []
        self.create_day_grid()

    def create_day_grid(self):
        """Создает сетку с днями"""
        for i in range(6):
            for j in range(7):
                frame = DirectFrame(
                    frameColor=self.config.background_color_choice,  # Тёмно-серый фон (можно поменять)
                    frameSize=(-0.07, 0.07, -0.07, 0.07),  # Размер под кнопку
                    pos=(-0.6 + j * 0.2, 0, 0.2 - i * 0.2),
                    parent=self.frame
                )

                # Создаём кнопку поверх фрейма
                button = DirectButton(
                    text="",
                    pos=(0, 0, -0.01),  # Позиция относительно фрейма (по центру)
                    scale=0.07,  # Масштаб кнопки
                    frameSize=(-1, 1, -1, 1),  # Подгоняем размер
                    command=self.select_day,
                    extraArgs=[i, j],
                    parent=frame,  # Делаем кнопку дочерним элементом фрейма
                    text_align=TextNode.ACenter,  # Центрируем текст
                    text_fg=(1, 1, 1, 1),  # Белый цвет текста
                    relief=None,  # Без рельефа
                )
                self.day_buttons.append(button)

    def update_ui(self, month, year, days_in_month, first_day_weekday, start_date, end_date):
        """Обновляет отображение календаря"""
        self.month_label.setText(datetime(year, month, 1).strftime("%B"))
        self.year_label.setText(str(year))

        for button in self.day_buttons:
            button["text"] = ""
            button["state"] = DGG.DISABLED

        day = 1
        for i in range(6):
            for j in range(7):
                if i == 0 and j < first_day_weekday:
                    continue
                if day > days_in_month:
                    break
                self.day_buttons[i * 7 + j]["text"] = str(day)
                self.day_buttons[i * 7 + j]["state"] = DGG.NORMAL
                day += 1

    def show(self):
        """Показывает календарь и скрывает кнопки выбора дат"""
        self.frame.show()
        self.open_calendar_first.hide()
        self.open_calendar_second.hide()
        self.start_help_text.hide()

    def hide(self):
        """Скрывает календарь и показывает кнопки выбора дат"""
        self.frame.hide()
        self.open_calendar_first.show()
        self.open_calendar_second.show()
        self.start_help_text.show()

    def calendar_popup(self, calendar_type):
        """Открывает календарь и скрывает кнопки выбора даты"""
        self.logic.calendar_popup(calendar_type)
        self.show()

    def select_day(self, i, j):
        """Выбирает день, обновляет данные и закрывает календарь"""
        self.logic.select_day(i, j)
        self.hide()

    def change_month(self, delta):
        """This method is called when the user clicks the buttons to change the month"""
        self.logic.change_month(delta)  # Call the corresponding method in `CalendarLogic`

    def change_year(self, delta):
        """This method is called when the user clicks the buttons to change the year"""
        self.logic.change_year(delta)  # Call the corresponding method in `CalendarLogic`
