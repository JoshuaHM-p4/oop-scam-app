import customtkinter as ctk
from tkcalendar import Calendar
from .calendar_model import CalendarModel, EventModel

class CalendarFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller