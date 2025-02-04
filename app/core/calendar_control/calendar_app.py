from app.core.calendar_control.calendar_logic import CalendarLogic
from app.core.calendar_control.calendar_ui import CalendarUI


class CalendarApp:
    def __init__(self):
        self.ui = CalendarUI()  # Create the UI first
        self.logic = CalendarLogic(self.ui)  # Pass the UI to CalendarLogic

        self.ui.logic = self.logic
