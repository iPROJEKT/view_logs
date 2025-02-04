from datetime import datetime

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DGG


class CalendarUI:
    def __init__(self):
        self.frame = DirectFrame(
            frameColor=(0, 0, 0, 1),
            frameSize=(-0.8, 0.8, -0.6, 0.6),
            pos=(0, 0, 0),
        )
        self.frame.hide()  # Начинаем с скрытого состояния

        self.month_label = OnscreenText(
            text="", pos=(0, 0.4), scale=0.07, parent=self.frame,
            fg=(1, 1, 1, 1)
        )
        self.year_label = OnscreenText(
            text="", pos=(0, 0.5), scale=0.07, parent=self.frame,
            fg=(1, 1, 1, 1)
        )

        self.prev_month_button = DirectButton(
            text="<", pos=(-0.4, 0, 0.4), scale=0.07, parent=self.frame,
            command=self.change_month, extraArgs=[-1]  # Calls `self.change_month` method when clicked
        )
        self.next_month_button = DirectButton(
            text=">", pos=(0.4, 0, 0.4), scale=0.07, parent=self.frame,
            command=self.change_month, extraArgs=[1]  # Calls `self.change_month` method when clicked
        )
        self.prev_year_button = DirectButton(
            text="<<", pos=(-0.4, 0, 0.5), scale=0.07, parent=self.frame,
            command=self.change_year, extraArgs=[-1]  # Calls `self.change_year` method when clicked
        )
        self.next_year_button = DirectButton(
            text=">>", pos=(0.4, 0, 0.5), scale=0.07, parent=self.frame,
            command=self.change_year, extraArgs=[1]  # Calls `self.change_year` method when clicked
        )

        self.day_buttons = []
        self.create_day_grid()

    def create_day_grid(self):
        """Создает сетку с днями"""
        for i in range(6):
            for j in range(7):
                button = DirectButton(
                    text="", pos=(-0.6 + j * 0.2, 0, 0.2 - i * 0.2), scale=0.08,
                    frameSize=(-1, 1, -1, 1),
                    command=self.select_day, extraArgs=[i, j], parent=self.frame,
                    text_fg=(1, 1, 1, 1), relief=None,
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
        """Показать календарь"""
        self.frame.show()

    def hide(self):
        """Скрыть календарь"""
        self.frame.hide()

    def change_month(self, delta):
        """This method is called when the user clicks the buttons to change the month"""
        self.logic.change_month(delta)  # Call the corresponding method in `CalendarLogic`

    def change_year(self, delta):
        """This method is called when the user clicks the buttons to change the year"""
        self.logic.change_year(delta)  # Call the corresponding method in `CalendarLogic`

    def select_day(self, i, j):
        """This method is called when the user clicks a day in the calendar"""
        self.logic.select_day(i, j)  # Call the corresponding method in `CalendarLogic`