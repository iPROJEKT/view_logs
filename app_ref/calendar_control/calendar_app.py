from app_ref.calendar_control.calendar_logic import CalendarLogic
from app_ref.calendar_control.calendar_ui import CalendarUI


class CalendarApp:
    def __init__(self, ui_node, config):
        self.ui = CalendarUI(config)  # Create the UI first
        self.logic = CalendarLogic(self.ui)  # Pass the UI to CalendarLogic

        self.ui.logic = self.logic
        self.ui_node = ui_node
