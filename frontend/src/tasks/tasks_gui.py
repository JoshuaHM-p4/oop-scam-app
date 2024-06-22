import tkinter as tk
from .tasks_gui import TasksModel

class TasksFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller