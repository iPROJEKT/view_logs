from app.core.calendar_control.calendar_logic import CalendarLogic
from app.core.calendar_control.calendar_ui import CalendarUI
from app.core.config import Config


class CalendarApp:
    def __init__(self, config):
        self.ui = CalendarUI(config)  # Create the UI first
        self.logic = CalendarLogic(self.ui)  # Pass the UI to CalendarLogic

        self.ui.logic = self.logic
