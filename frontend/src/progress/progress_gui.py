import customtkinter as ctk
from .progress_model import ProgressModel

class ProgressFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller