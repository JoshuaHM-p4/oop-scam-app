import tkinter as tk
from .progress_model import ProgressModel

class ProgressFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller