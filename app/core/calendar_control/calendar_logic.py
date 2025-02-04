from datetime import datetime


class CalendarLogic:
    def __init__(self, ui):
        self.ui = ui
        self.current_date = datetime.now()
        self.year = self.current_date.year
        self.month = self.current_date.month
        self.start_date = None
        self.end_date = None
        self.selecting_start_date = True  # По умолчанию выбираем начальную дату
        self.update_calendar()

    def update_calendar(self):
        """Обновляет интерфейс календаря"""
        days_in_month = self.get_days_in_month(self.year, self.month)
        first_day_weekday = datetime(self.year, self.month, 1).weekday()
        first_day_weekday = (first_day_weekday + 1) % 7
        self.ui.update_ui(self.month, self.year, days_in_month, first_day_weekday, self.start_date, self.end_date)  # Now it will work

    @staticmethod
    def get_days_in_month(year, month):
        """Возвращает количество дней в месяце"""
        if month == 2:
            return 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        return 31

    def change_month(self, delta):
        """Переключает месяц вперед или назад"""
        self.month += delta
        if self.month > 12:
            self.month = 1
            self.year += 1
        elif self.month < 1:
            self.month = 12
            self.year -= 1
        self.update_calendar()

    def change_year(self, delta):
        """Переключает год вперед или назад"""
        self.year += delta
        self.update_calendar()

    def select_day(self, i, j):
        """Выбирает день в календаре"""
        first_day_weekday = (datetime(self.year, self.month, 1).weekday() + 1) % 7
        day = (i * 7) + j - first_day_weekday + 1
        days_in_month = self.get_days_in_month(self.year, self.month)

        if 1 <= day <= days_in_month:
            selected_date = datetime(self.year, self.month, day)

            if self.selecting_start_date:
                self.start_date = selected_date
                print(f"Выбрана начальная дата: {self.start_date.date()}")
            else:
                self.end_date = selected_date
                print(f"Выбрана конечная дата: {self.end_date.date()}")

            self.ui.hide()
            self.update_calendar()

    def on_date_selected(self):
        """Обработчик выбора диапазона дат"""
        if self.start_date and self.end_date:
            print(f"Выбран диапазон: {self.start_date.date()} - {self.end_date.date()}")
        elif self.start_date:
            print(f"Выбрана начальная дата: {self.start_date.date()}")
