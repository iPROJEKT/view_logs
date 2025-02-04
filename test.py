from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import OnscreenText, DirectButton, DGG
from datetime import datetime


class CalendarApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Настройка камеры
        self.disableMouse()
        self.camera.setPos(0, -15, 10)
        self.camera.lookAt(0, 0, 0)

        # Текущая дата
        self.current_date = datetime.now()
        self.year = self.current_date.year
        self.month = self.current_date.month
        self.day = self.current_date.day

        # Создаем текстовые метки для отображения месяца и года
        self.month_label = OnscreenText(text="", pos=(-0.8, 0.8), scale=0.1, align=TextNode.ALeft)
        self.year_label = OnscreenText(text="", pos=(0.8, 0.8), scale=0.1, align=TextNode.ARight)

        # Кнопки для переключения месяцев и годов
        self.prev_month_button = DirectButton(text="<", pos=(-0.9, 0, 0.9), scale=0.1, command=self.change_month, extraArgs=[-1])
        self.next_month_button = DirectButton(text=">", pos=(0.9, 0, 0.9), scale=0.1, command=self.change_month, extraArgs=[1])
        self.prev_year_button = DirectButton(text="<<", pos=(-0.9, 0, 0.7), scale=0.1, command=self.change_year, extraArgs=[-1])
        self.next_year_button = DirectButton(text=">>", pos=(0.9, 0, 0.7), scale=0.1, command=self.change_year, extraArgs=[1])

        # Сетка для отображения дней месяца
        self.day_buttons = []
        self.create_day_grid()

        # Обновляем отображение календаря
        self.update_calendar()

    def create_day_grid(self):
        """Создаем сетку для отображения дней месяца."""
        for i in range(6):  # 6 строк (максимум 6 недель в месяце)
            for j in range(7):  # 7 столбцов (дни недели)
                button = DirectButton(
                    text="",
                    pos=(-0.6 + j * 0.2, 0, 0.5 - i * 0.2),
                    scale=0.08,
                    frameSize=(-1, 1, -1, 1),
                    command=self.select_day,
                    extraArgs=[i, j]  # Передаем координаты ячейки (строка, столбец)
                )
                self.day_buttons.append(button)

    def update_calendar(self):
        """Обновляем отображение календаря."""
        # Обновляем метки месяца и года
        self.month_label.setText(self.current_date.strftime("%B"))
        self.year_label.setText(str(self.year))

        # Получаем количество дней в текущем месяце
        days_in_month = self.get_days_in_month(self.year, self.month)

        # Получаем день недели для первого дня месяца
        first_day_weekday = datetime(self.year, self.month, 1).weekday()  # 0 = понедельник, 6 = воскресенье

        # Очищаем кнопки
        for button in self.day_buttons:
            button["text"] = ""
            button["state"] = DGG.DISABLED

        # Заполняем кнопки днями месяца
        day = 1
        for i in range(6):
            for j in range(7):
                if i == 0 and j < first_day_weekday:
                    continue  # Пропускаем пустые ячейки до первого дня месяца
                if day > days_in_month:
                    break  # Прерываем, если дни месяца закончились
                self.day_buttons[i * 7 + j]["text"] = str(day)
                self.day_buttons[i * 7 + j]["state"] = DGG.NORMAL
                day += 1

    def get_days_in_month(self, year, month):
        """Возвращает количество дней в месяце."""
        if month == 2:  # Февраль
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29  # Високосный год
            else:
                return 28
        elif month in [4, 6, 9, 11]:  # Апрель, июнь, сентябрь, ноябрь
            return 30
        else:
            return 31

    def change_month(self, delta):
        """Переключаем месяц."""
        self.month += delta
        if self.month > 12:
            self.month = 1
            self.year += 1
        elif self.month < 1:
            self.month = 12
            self.year -= 1
        self.current_date = datetime(self.year, self.month, 1)
        self.update_calendar()

    def change_year(self, delta):
        """Переключаем год."""
        self.year += delta
        self.current_date = datetime(self.year, self.month, 1)
        self.update_calendar()

    def select_day(self, i, j):
        """Обрабатываем выбор дня."""
        # Получаем день недели для первого дня месяца
        first_day_weekday = datetime(self.year, self.month, 1).weekday()  # 0 = понедельник, 6 = воскресенье

        # Вычисляем выбранный день
        if i == 0 and j < first_day_weekday:
            return  # Пропускаем пустые ячейки до первого дня месяца

        day = (i * 7) + j - first_day_weekday + 1
        days_in_month = self.get_days_in_month(self.year, self.month)

        if day < 1 or day > days_in_month:
            return  # Пропускаем пустые ячейки после последнего дня месяца

        self.day = day
        print(f"Выбрана дата: {self.day:02d}.{self.month:02d}.{self.year}")


app = CalendarApp()
app.run()