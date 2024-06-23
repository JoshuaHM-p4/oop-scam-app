import customtkinter as ctk
from .tasks_model import TasksModel

class TasksFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller