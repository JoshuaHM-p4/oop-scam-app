import tkinter as tk
from .templates_model import TemplateModel, HomeworkModel, MathModel, LetterModel, EssayModel

class TemplatesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller