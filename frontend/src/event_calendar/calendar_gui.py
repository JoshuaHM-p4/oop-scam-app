import tkinter as tk
from tkcalendar import Calendar
from .calendar_model import CalendarModel, EventModel

class CalendarFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller