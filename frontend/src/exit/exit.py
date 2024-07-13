import customtkinter as ctk
from user_model import UserModel

class ExitFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

    def tkraise(self):
        super().tkraise()
        # Session Attributes
        self.controller.quit()