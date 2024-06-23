import customtkinter as ctk
from .templates_model import TemplateModel, HomeworkModel, MathModel, LetterModel, EssayModel

class TemplatesFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller